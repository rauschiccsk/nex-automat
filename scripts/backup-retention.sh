#!/usr/bin/env bash
#
# backup-retention.sh — apply GFS retention policy to both restic repos.
#
# Usage:  sudo ./scripts/backup-retention.sh
#         (typically invoked nightly from /etc/cron.d/nex-backup)
#
# Policy: keep last 7 daily + 4 weekly + 6 monthly per customer (Phase D.6).
# Prune (compact) runs once per repo at the end (expensive, but local repo
# benefits the most — frees disk).

set -euo pipefail

CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"
RESTIC_LOCAL="${RESTIC_LOCAL:-/data/backups/restic}"
B2_CREDS_FILE="${B2_CREDS_FILE:-/root/.backup-b2}"
PASSPHRASE_FILE="${PASSPHRASE_FILE:-/root/.backup-passphrase}"

[[ -f "$B2_CREDS_FILE" ]]   || { echo "ERROR: ${B2_CREDS_FILE} missing"; exit 1; }
[[ -f "$PASSPHRASE_FILE" ]] || { echo "ERROR: ${PASSPHRASE_FILE} missing"; exit 1; }

set -a
# shellcheck disable=SC1091
source "$B2_CREDS_FILE"
set +a
export RESTIC_PASSWORD_FILE="$PASSPHRASE_FILE"

# Discover onboarded customers from /opt/customers/
mapfile -t SLUGS < <(find "$CUSTOMERS_ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | sort)
[[ "${#SLUGS[@]}" -gt 0 ]] || { echo "No customers found in ${CUSTOMERS_ROOT}"; exit 0; }

apply_forget() {
    local repo="$1"
    local repo_label="$2"
    echo "[retention] === ${repo_label} ==="
    for slug in "${SLUGS[@]}"; do
        echo "[retention]   forget customer=${slug}..."
        RESTIC_REPOSITORY="$repo" \
            restic forget \
                --tag "customer=${slug}" \
                --keep-daily 7 \
                --keep-weekly 4 \
                --keep-monthly 6 \
                --quiet
    done
}

# 1. Local repo — forget + prune
apply_forget "$RESTIC_LOCAL" "local"
echo "[retention] pruning local repo (this may take a minute)..."
RESTIC_REPOSITORY="$RESTIC_LOCAL" restic prune --quiet

# 2. B2 repo — forget + prune (B2 storage costs accrue per-byte, prune matters)
apply_forget "b2:${B2_BUCKET}:/" "b2"
echo "[retention] pruning b2 repo (this may take longer due to network)..."
RESTIC_REPOSITORY="b2:${B2_BUCKET}:/" restic prune --quiet

echo "[retention] DONE"
