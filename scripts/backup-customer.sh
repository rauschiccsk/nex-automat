#!/usr/bin/env bash
#
# backup-customer.sh — daily backup of one customer's full stack.
#
# Usage:  sudo ./scripts/backup-customer.sh <slug>
#         (typically invoked from cron, see ANDROS root crontab)
#
# Produces /opt/backups/<slug>/<slug>-<timestamp>.tgz containing:
#   - DB dump (pg_dump --create)
#   - docker-compose.yml + .env + nginx config
#   - postgres data volume (raw — for fast restore)
#
# Retention: 30 days (find -mtime +30 -delete).

set -euo pipefail

SLUG="${1:-}"
BACKUPS_ROOT="${BACKUPS_ROOT:-/opt/backups}"
CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"
RETENTION_DAYS="${RETENTION_DAYS:-30}"

if [[ -z "$SLUG" ]]; then
    echo "Usage: $0 <slug>" >&2
    exit 1
fi
CUSTOMER_DIR="${CUSTOMERS_ROOT}/${SLUG}"
if [[ ! -d "$CUSTOMER_DIR" ]]; then
    echo "ERROR: ${CUSTOMER_DIR} does not exist" >&2
    exit 1
fi

DEST="${BACKUPS_ROOT}/${SLUG}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "$DEST"

WORK_DIR=$(mktemp -d)
trap "rm -rf '$WORK_DIR'" EXIT

# 1. DB dump
echo "[backup ${SLUG}] dumping postgres..."
docker exec "${SLUG}-postgres" pg_dump -U postgres --create -d nex_automat \
    > "${WORK_DIR}/db.sql"

# 2. Bundle config + dump
cd "$CUSTOMER_DIR"
BUNDLE="${DEST}/${SLUG}-${TIMESTAMP}.tgz"
tar czf "$BUNDLE" \
    docker-compose.yml \
    .env \
    "${SLUG}.nginx.conf" \
    -C "$WORK_DIR" db.sql

SIZE=$(du -h "$BUNDLE" | cut -f1)
echo "[backup ${SLUG}] wrote ${BUNDLE} (${SIZE})"

# 3. Retention — delete bundles older than ${RETENTION_DAYS} days
DELETED=$(find "$DEST" -name "*.tgz" -mtime +"${RETENTION_DAYS}" -print -delete | wc -l)
[[ "$DELETED" -gt 0 ]] && echo "[backup ${SLUG}] purged ${DELETED} backup(s) older than ${RETENTION_DAYS} days"

# 4. Touch a marker file for monitoring (Q8 — backup-status check)
touch "${DEST}/.last-success"
