#!/usr/bin/env bash
#
# backup-server.sh — daily backup of server infrastructure to local + B2.
#
# Backs up everything needed to rebuild the Andros server from scratch:
#   /etc          — nginx, cron, netplan, certbot, systemd
#   /opt/nex-automat      — alertmanager, grafana, prometheus, temporal configs
#   /opt/stalwart         — mail server config + data + DKIM keys
#   /opt/customers        — full customer dirs (DB + nginx + inbox + telegram)
#   /opt/websites /opt/apps /opt/uat /opt/prod /opt/infra
#   /opt/jitsi-meet /opt/rustdesk
#   /opt/projects/nex-horizont  — only project without GitHub remote
#   /home/andros   — SSH keys, credentials, wireguard, knowledge, scripts
#   /home/icc      — Vaultwarden data, knowledge
#   /root          — B2 creds, passphrase, system config
#   /data/docker-volumes/postgres  — nex-command postgres (live bind-mount)
#   /data/docker-volumes/qdrant    — nex-qdrant (live bind-mount)
#   DB_DUMP_DIR   — pg_dump of all production app databases (see list below)
#
# Production databases dumped (pg_dump -Fc):
#   nex-studio-db-1, nex-payroll-db, nex-asistent-postgres,
#   icc-website-db-1, icc-website-staging-db-1, delphi-studio-db,
#   icc-inbox-db, andros-inbox-db, prod-inbox-postgres, uat-inbox-postgres
#
# Excludes (too large or easily regenerated):
#   /data/docker-volumes/ollama      — 30 GB models, re-downloadable
#   /data/docker-volumes/prometheus  — stale (live data in Docker named volume)
#   /data/docker-volumes/grafana     — stale (dashboards are code in /opt/nex-automat/)
#   /data/vms/                       — 155 GB Windows VMs, separate strategy
#   /home/andros/emcenter            — bind-mount of /data (duplicate)
#   /home/andros/.vscode-server      — VS Code IDE binaries, regeneratable
#   /home/andros/.npm                — npm cache, regeneratable
#   /home/andros/.local/lib          — Python packages, regeneratable
#   /home/andros/.local/share/claude — Claude Code transcript DB, regeneratable
#   /home/andros/.local/share/pipx   — pipx tools, regeneratable
#   github runners, node_modules, __pycache__, .cache
#
# Usage:  sudo /opt/nex-automat-src/scripts/backup-server.sh
# Cron:   see /etc/cron.d/nex-backup (runs at 01:00 daily)

set -euo pipefail

RESTIC_LOCAL="${RESTIC_LOCAL:-/data/backups/restic-server}"
B2_CREDS_FILE="${B2_CREDS_FILE:-/root/.backup-b2}"
PASSPHRASE_FILE="${PASSPHRASE_FILE:-/root/.backup-passphrase}"
TEXTFILE_DIR="${TEXTFILE_DIR:-/var/lib/node-exporter/textfile}"
B2_PATH="server-infra"

[[ -f "$B2_CREDS_FILE" ]]   || { echo "ERROR: ${B2_CREDS_FILE} missing"; exit 1; }
[[ -f "$PASSPHRASE_FILE" ]] || { echo "ERROR: ${PASSPHRASE_FILE} missing"; exit 1; }

set -a
# shellcheck disable=SC1091
source "$B2_CREDS_FILE"
set +a
export RESTIC_PASSWORD_FILE="$PASSPHRASE_FILE"

DB_DUMP_DIR=$(mktemp -d)

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
        -d "text=🚨 <b>SERVER BACKUP FAILED</b>%0Ahost: <code>$(hostname)</code>%0A${msg}" \
        >/dev/null || true
}

trap 'rc=$?; rm -rf "$DB_DUMP_DIR"; [[ $rc -ne 0 ]] && notify_failure "exit code ${rc} on host $(hostname)"' EXIT

# Initialize restic repos on first run
init_if_needed() {
    local repo="$1"
    if ! RESTIC_REPOSITORY="$repo" restic cat config &>/dev/null 2>&1; then
        echo "[server-backup] initializing new repo: $repo"
        RESTIC_REPOSITORY="$repo" restic init
    fi
}

init_if_needed "$RESTIC_LOCAL"
init_if_needed "b2:${B2_BUCKET}:/${B2_PATH}"

# --- pg_dump for all production app databases ---
# Format: "container_name:db_user:db_name"
APP_DBS=(
    "nex-studio-db-1:nexstudio:nexstudio"
    "nex-studio-uat-db-1:nexstudio:nexstudio"
    "nex-payroll-db:nex_payroll:nex_payroll"
    "nex-asistent-postgres:nex_asistent:nex_asistent"
    "icc-website-db-1:icc_website:icc_website"
    "icc-website-staging-db-1:icc_website:icc_website_staging"
    "delphi-studio-db:delphi:delphi_studio"
    "icc-inbox-db:nex_inbox_icc:nex_inbox_icc"
    "andros-inbox-db:nex_inbox_andros:nex_inbox_andros"
    "prod-inbox-postgres:nex_inbox:nex_inbox_mager"
    "uat-inbox-postgres:nex_inbox:nex_inbox_dev"
)

echo "[server-backup] dumping application databases..."
for entry in "${APP_DBS[@]}"; do
    container="${entry%%:*}"
    rest="${entry#*:}"
    user="${rest%%:*}"
    dbname="${rest#*:}"

    if docker inspect "$container" &>/dev/null; then
        outfile="${DB_DUMP_DIR}/${container}.dump"
        echo "[server-backup]   pg_dump ${container} (${dbname})..."
        if docker exec "$container" pg_dump -U "$user" -Fc "$dbname" > "$outfile" 2>/dev/null; then
            echo "[server-backup]   → $(du -h "$outfile" | cut -f1)"
        else
            echo "[server-backup]   WARNING: pg_dump failed for ${container}, skipping"
            rm -f "$outfile"
        fi
    else
        echo "[server-backup]   skipping ${container} (not running)"
    fi
done

# Paths to back up — filter to those that actually exist
CANDIDATE_PATHS=(
    /etc
    /opt/nex-automat
    /opt/stalwart
    /opt/customers
    /opt/websites
    /opt/apps
    /opt/uat
    /opt/prod
    /opt/infra
    /opt/jitsi-meet
    /opt/rustdesk
    /opt/projects/nex-horizont
    /home/andros
    /home/icc
    /root
    /data/docker-volumes/postgres
    /data/docker-volumes/qdrant
    /data/docker-volumes/icc
    /data/docker-volumes/temporal
    /data/docker-volumes/alertmanager
    "$DB_DUMP_DIR"
)

BACKUP_PATHS=()
for p in "${CANDIDATE_PATHS[@]}"; do
    [[ -e "$p" ]] && BACKUP_PATHS+=("$p")
done

echo "[server-backup] restic → local..."

RESTIC_REPOSITORY="$RESTIC_LOCAL" \
    restic backup \
    "${BACKUP_PATHS[@]}" \
    --tag "server-infra" \
    --host "andros" \
    --exclude '/home/andros/.cache' \
    --exclude '/home/andros/snap' \
    --exclude '/home/andros/emcenter' \
    --exclude '/home/andros/.vscode-server' \
    --exclude '/home/andros/.npm' \
    --exclude '/home/andros/.local/lib' \
    --exclude '/home/andros/.local/share/claude' \
    --exclude '/home/andros/.local/share/pipx' \
    --exclude '/home/icc/.cache' \
    --exclude '/data/backup/imac-restic' \
    --exclude '*/node_modules' \
    --exclude '*/__pycache__' \
    --exclude '*.pyc' \
    --exclude '*.pyo' \
    --exclude-if-present '.nobackup' \
    --quiet

echo "[server-backup] restic copy → B2..."
RESTIC_REPOSITORY="b2:${B2_BUCKET}:/${B2_PATH}" \
RESTIC_FROM_REPOSITORY="$RESTIC_LOCAL" \
RESTIC_FROM_PASSWORD_FILE="$PASSPHRASE_FILE" \
    restic copy \
    --tag "server-infra" \
    --host "andros" \
    --quiet

# Retention: 7 daily, 4 weekly, 6 monthly (GFS policy, same as customer backups)
echo "[server-backup] applying retention..."
for repo in "$RESTIC_LOCAL" "b2:${B2_BUCKET}:/${B2_PATH}"; do
    RESTIC_REPOSITORY="$repo" \
        restic forget \
        --tag "server-infra" \
        --keep-daily 7 \
        --keep-weekly 4 \
        --keep-monthly 6 \
        --prune \
        --quiet
done

# Prometheus textfile metric for Grafana monitoring
mkdir -p "$TEXTFILE_DIR"
cat > "${TEXTFILE_DIR}/nex_backup.server.prom.tmp" <<EOF
# HELP nex_backup_last_success_timestamp_seconds Unix timestamp of last successful backup
# TYPE nex_backup_last_success_timestamp_seconds gauge
nex_backup_last_success_timestamp_seconds{customer="server-infra"} $(date +%s)
EOF
mv "${TEXTFILE_DIR}/nex_backup.server.prom.tmp" "${TEXTFILE_DIR}/nex_backup.server.prom"

echo "[server-backup] DONE"
trap - EXIT
rm -rf "$DB_DUMP_DIR"
