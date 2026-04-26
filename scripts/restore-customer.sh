#!/usr/bin/env bash
#
# restore-customer.sh — restore one customer's stack from a backup bundle.
#
# Usage:  sudo ./scripts/restore-customer.sh <slug> <backup-file.tgz>
#
# Use cases:
#   1. Disaster recovery on same ANDROS  (rollback to yesterday's data)
#   2. Self-host migration to customer's own server (extract + run elsewhere)
#
# WARNING: destructive — wipes existing customer DB data before restore.
# Confirms via prompt unless RESTORE_FORCE=1 in env.

set -euo pipefail

SLUG="${1:-}"
BUNDLE="${2:-}"
CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"

if [[ -z "$SLUG" || -z "$BUNDLE" ]]; then
    echo "Usage: $0 <slug> <backup-file.tgz>" >&2
    exit 1
fi
if [[ ! -f "$BUNDLE" ]]; then
    echo "ERROR: ${BUNDLE} not found" >&2
    exit 1
fi
CUSTOMER_DIR="${CUSTOMERS_ROOT}/${SLUG}"

# Confirm destructive op
if [[ "${RESTORE_FORCE:-0}" != "1" ]]; then
    echo "WARNING: This will WIPE current data for customer '${SLUG}' and"
    echo "         restore from ${BUNDLE}"
    read -rp "Type 'yes' to continue: " CONFIRM
    [[ "$CONFIRM" == "yes" ]] || { echo "Aborted."; exit 1; }
fi

# 1. Extract bundle
WORK_DIR=$(mktemp -d)
trap "rm -rf '$WORK_DIR'" EXIT
tar xzf "$BUNDLE" -C "$WORK_DIR"
echo "[restore ${SLUG}] bundle extracted to ${WORK_DIR}"

# 2. Stop containers (DB will be wiped)
if [[ -d "$CUSTOMER_DIR" ]]; then
    cd "$CUSTOMER_DIR"
    docker compose down --volumes 2>/dev/null || true
else
    mkdir -p "$CUSTOMER_DIR"
fi

# 3. Restore configs
cp "${WORK_DIR}/docker-compose.yml" "${CUSTOMER_DIR}/"
cp "${WORK_DIR}/.env" "${CUSTOMER_DIR}/"
chmod 600 "${CUSTOMER_DIR}/.env"
cp "${WORK_DIR}/${SLUG}.nginx.conf" "${CUSTOMER_DIR}/" 2>/dev/null || true
echo "[restore ${SLUG}] configs restored"

# 4. Start postgres only, wait for healthy, then load DB dump
cd "$CUSTOMER_DIR"
docker compose up -d postgres
echo "[restore ${SLUG}] waiting for postgres healthy..."
for i in $(seq 1 30); do
    HEALTH=$(docker inspect --format '{{.State.Health.Status}}' "${SLUG}-postgres" 2>/dev/null || echo "starting")
    [[ "$HEALTH" == "healthy" ]] && break
    sleep 2
done
[[ "$HEALTH" != "healthy" ]] && { echo "ERROR: postgres did not become healthy"; exit 1; }

echo "[restore ${SLUG}] loading DB dump..."
docker exec -i "${SLUG}-postgres" psql -U postgres < "${WORK_DIR}/db.sql"

# 5. Start remaining services
docker compose up -d
echo "[restore ${SLUG}] all services started"

# 6. Healthcheck
sleep 5
HEALTH_URL="https://${SLUG}.nex-automat.isnex.eu/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" || echo "000")
echo "[restore ${SLUG}] healthcheck ${HEALTH_URL} → HTTP ${STATUS}"
[[ "$STATUS" == "200" ]] && echo "[restore ${SLUG}] DONE" || echo "WARNING: healthcheck failed"
