#!/usr/bin/env bash
#
# backup-customer.sh — daily backup of one customer's stack via restic.
#
# Usage:  sudo ./scripts/backup-customer.sh <slug>
#         (typically invoked from cron via /etc/cron.d/nex-backup)
#
# Architecture (per Phase D.6, see KB DECISIONS.md D-024):
#   1. pg_dump customer DB (custom format, compressed) + bundle .env +
#      docker-compose.yml + nginx config into a temp dir.
#   2. restic backup → LOCAL repo at /data/backups/restic (fast restore).
#   3. restic copy LOCAL → B2 cloud repo (offsite DR).
#   4. Write success timestamp to node-exporter textfile collector for
#      Prometheus monitoring.
#
# On failure: Telegram alert via existing nex-alertmanager bot (curl direct).
#
# Required state:
#   /root/.backup-b2          — B2 creds (B2_ACCOUNT_ID, B2_ACCOUNT_KEY, B2_BUCKET)
#   /root/.backup-passphrase  — restic repo passphrase (shared by local + B2)

set -euo pipefail

SLUG="${1:-}"
CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"
RESTIC_LOCAL="${RESTIC_LOCAL:-/data/backups/restic}"
B2_CREDS_FILE="${B2_CREDS_FILE:-/root/.backup-b2}"
PASSPHRASE_FILE="${PASSPHRASE_FILE:-/root/.backup-passphrase}"
TEXTFILE_DIR="${TEXTFILE_DIR:-/var/lib/node-exporter/textfile}"

if [[ -z "$SLUG" ]]; then
    echo "Usage: $0 <slug>" >&2
    exit 1
fi
CUSTOMER_DIR="${CUSTOMERS_ROOT}/${SLUG}"
if [[ ! -d "$CUSTOMER_DIR" ]]; then
    echo "ERROR: ${CUSTOMER_DIR} does not exist" >&2
    exit 1
fi
[[ -f "$B2_CREDS_FILE" ]]    || { echo "ERROR: ${B2_CREDS_FILE} missing"; exit 1; }
[[ -f "$PASSPHRASE_FILE" ]]  || { echo "ERROR: ${PASSPHRASE_FILE} missing"; exit 1; }

# Source B2 creds (B2_ACCOUNT_ID, B2_ACCOUNT_KEY, B2_BUCKET)
set -a
# shellcheck disable=SC1091
source "$B2_CREDS_FILE"
set +a
export RESTIC_PASSWORD_FILE="$PASSPHRASE_FILE"

# Telegram failure notifier — uses existing alertmanager Telegram bot.
# Pulls bot_token + chat_id from /opt/nex-automat/alertmanager/alertmanager.yml
# (no extra config required).
notify_failure() {
    local msg="$1"
    local cfg="/opt/nex-automat/alertmanager/alertmanager.yml"
    [[ -r "$cfg" ]] || return 0
    local token chat
    token=$(awk '/bot_token:/ {gsub(/[\x27 ]/, "", $2); print $2; exit}' "$cfg")
    chat=$(awk '/chat_id:/ {print $2; exit}' "$cfg")
    [[ -n "$token" && -n "$chat" ]] || return 0
    curl -s -X POST "https://api.telegram.org/bot${token}/sendMessage" \
        -d "chat_id=${chat}" \
        -d "parse_mode=HTML" \
        -d "text=🚨 <b>BACKUP FAILED</b>%0Acustomer: <code>${SLUG}</code>%0A${msg}" \
        >/dev/null || true
}

trap 'rc=$?; [[ $rc -ne 0 ]] && notify_failure "exit code ${rc} on host $(hostname)"' EXIT

# 1. Build a working dir with everything to back up
WORK_DIR=$(mktemp -d)
trap 'rc=$?; rm -rf "$WORK_DIR"; [[ $rc -ne 0 ]] && notify_failure "exit code ${rc} on host $(hostname)"' EXIT

echo "[backup ${SLUG}] dumping postgres..."
docker exec "${SLUG}-postgres" pg_dump -U postgres -Fc -d nex_automat \
    > "${WORK_DIR}/db.dump"

cp "${CUSTOMER_DIR}/.env"               "${WORK_DIR}/env"      # avoid .env hidden file
cp "${CUSTOMER_DIR}/docker-compose.yml" "${WORK_DIR}/"
cp "${CUSTOMER_DIR}/${SLUG}.nginx.conf" "${WORK_DIR}/" 2>/dev/null || true

# 2. Backup to LOCAL repo (fast)
echo "[backup ${SLUG}] restic → local..."
RESTIC_REPOSITORY="$RESTIC_LOCAL" \
    restic backup "$WORK_DIR" \
    --tag "customer=${SLUG}" \
    --host "andros" \
    --quiet

# 3. Copy LOCAL → B2 (offsite). Both repos use the same passphrase, but
# restic needs them set explicitly via FROM_* env vars for source.
echo "[backup ${SLUG}] restic copy → B2..."
RESTIC_REPOSITORY="b2:${B2_BUCKET}:/" \
RESTIC_FROM_REPOSITORY="$RESTIC_LOCAL" \
RESTIC_FROM_PASSWORD_FILE="$PASSPHRASE_FILE" \
    restic copy \
    --tag "customer=${SLUG}" \
    --host "andros" \
    --quiet

# 4. Write success metric for Prometheus textfile collector (atomic write)
mkdir -p "$TEXTFILE_DIR"
cat > "${TEXTFILE_DIR}/nex_backup.${SLUG}.prom.tmp" <<EOF
# HELP nex_backup_last_success_timestamp_seconds Unix timestamp of last successful backup
# TYPE nex_backup_last_success_timestamp_seconds gauge
nex_backup_last_success_timestamp_seconds{customer="${SLUG}"} $(date +%s)
EOF
mv "${TEXTFILE_DIR}/nex_backup.${SLUG}.prom.tmp" "${TEXTFILE_DIR}/nex_backup.${SLUG}.prom"

echo "[backup ${SLUG}] DONE"
trap - EXIT
