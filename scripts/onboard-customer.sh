#!/usr/bin/env bash
#
# onboard-customer.sh — provision a fully isolated NEX Manager stack
#                       for a new customer on ANDROS.
#
# URL pattern: <slug>.isnex.eu (single-level subdomain — covered by
# Cloudflare Universal SSL for *.isnex.eu, no sub-zone delegation).
# Each customer gets own per-customer LE cert via DNS-01 challenge.
#
# Usage:  sudo ./scripts/onboard-customer.sh <slug> [--skip-dns-prompt]
#
# Flags:
#   --skip-dns-prompt   Skip interactive ENTER pause after DNS instruction
#                       (use when DNS record was already added before running).
#
# Output:
#   Initial admin credentials are admin/admin (from migration 002 seed).
#   Director logs in immediately after onboarding, changes password via UI
#   (System → Užívatelia → admin → Edit password) and creates customer users.
#
# Prerequisites on ANDROS:
#   - Docker + docker compose v2
#   - nginx running on host (port 80, 443)
#   - Cloudflare API token at /root/.cloudflare/credentials with
#     Zone:DNS:Edit permission for isnex.eu
#   - Docker network 'nex-proxy-net' (one-time setup, already created)
#   - Migrations 001-016 at /opt/nex-automat-src/database/migrations/
#   - Images nex-manager-backend:latest + nex-manager-frontend:latest

set -euo pipefail

SLUG="${1:-}"
SKIP_DNS_PROMPT=0
for arg in "$@"; do
    [[ "$arg" == "--skip-dns-prompt" ]] && SKIP_DNS_PROMPT=1
done
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TEMPLATE_DIR="${REPO_ROOT}/deployment/customer-template"
MIGRATIONS_DIR="${REPO_ROOT}/database/migrations"
CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"
NGINX_CONF_DIR="${NGINX_CONF_DIR:-/etc/nginx/conf.d}"
CF_CREDENTIALS="${CF_CREDENTIALS:-/root/.cloudflare/credentials}"
CERT_EMAIL="${CERT_EMAIL:-iccforai@gmail.com}"

# ──────────────────────────────────────────────────────────────────────
# 1. Validate slug
# ──────────────────────────────────────────────────────────────────────
if [[ -z "$SLUG" ]]; then
    echo "Usage: $0 <slug>" >&2
    echo "  slug must be lowercase, 3-15 chars, alphanumeric + hyphens" >&2
    exit 1
fi
if ! [[ "$SLUG" =~ ^[a-z0-9][a-z0-9-]{1,13}[a-z0-9]$ ]]; then
    echo "ERROR: slug '$SLUG' invalid (lowercase, 3-15 chars, no leading/trailing hyphen)" >&2
    exit 1
fi
DOMAIN="${SLUG}.isnex.eu"
CUSTOMER_DIR="${CUSTOMERS_ROOT}/${SLUG}"
if [[ -d "$CUSTOMER_DIR" ]]; then
    echo "ERROR: ${CUSTOMER_DIR} already exists — refusing to overwrite" >&2
    exit 1
fi
if docker ps -a --format '{{.Names}}' | grep -qE "^${SLUG}-(postgres|backend|frontend)$"; then
    echo "ERROR: containers ${SLUG}-* already exist — clean up first" >&2
    exit 1
fi

echo "[onboard] Provisioning customer '${SLUG}' at ${DOMAIN}"

# ──────────────────────────────────────────────────────────────────────
# 2. Generate secrets
# ──────────────────────────────────────────────────────────────────────
POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-32)
JWT_SECRET_KEY=$(openssl rand -base64 64 | tr -d '\n')
# Admin password = "admin" from migration 002 seed (admin/admin pattern).
# Director changes via UI immediately after first login.

# Allocate frontend port from internal range 19000-19499 (host-nginx routing
# only, bound to 127.0.0.1, not internet-exposed). Cross-reference TWO sources:
#   1. Already-allocated ports in existing /opt/customers/*/.env (catches
#      configured-but-temporarily-stopped customers — a previous bug)
#   2. Currently-listening ports via ss (catches non-customer host services)
USED_PORTS=$(grep -h "^FRONTEND_PORT=" "${CUSTOMERS_ROOT}"/*/.env 2>/dev/null | cut -d= -f2 | sort -un)
FRONTEND_PORT=19000
while { echo "$USED_PORTS" | grep -qx "$FRONTEND_PORT"; } \
   || ss -tlnp 2>/dev/null | grep -q ":${FRONTEND_PORT}\b"; do
    FRONTEND_PORT=$((FRONTEND_PORT + 1))
    if [[ $FRONTEND_PORT -ge 19500 ]]; then
        echo "ERROR: no free port in 19000-19499 range" >&2
        exit 1
    fi
done
echo "[onboard] Allocated FRONTEND_PORT=${FRONTEND_PORT} (127.0.0.1 only)"

# ──────────────────────────────────────────────────────────────────────
# 3. Create customer directory + render templates
# ──────────────────────────────────────────────────────────────────────
mkdir -p "$CUSTOMER_DIR"
cd "$CUSTOMER_DIR"

cat > .env <<EOF
SLUG=${SLUG}
IMAGE_TAG=latest
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
FRONTEND_PORT=${FRONTEND_PORT}
EOF
chmod 600 .env

cp "${TEMPLATE_DIR}/docker-compose.yml.template" docker-compose.yml

SLUG="${SLUG}" FRONTEND_PORT="${FRONTEND_PORT}" envsubst '${SLUG} ${FRONTEND_PORT}' \
    < "${TEMPLATE_DIR}/nginx-snippet.conf.template" \
    > "${SLUG}.nginx.conf"

echo "[onboard] Generated ${CUSTOMER_DIR}/.env, docker-compose.yml, ${SLUG}.nginx.conf"

# Migration data drop point — backend container mounts this dir as /migration.
# Operator drops extracted Btrieve JSON files here (per category subdir) before
# triggering /api/migration/run from the UI.
mkdir -p "${CUSTOMER_DIR}/migration"
echo "[onboard] Created migration data dir: ${CUSTOMER_DIR}/migration/"

# Hand off ownership to the deploy user (who invoked sudo) so the GitHub
# Actions runner can read .env without sudo. Mode 600 on .env preserves
# secret confidentiality — only the deploy user (and root) can read it.
DEPLOY_USER="${SUDO_USER:-$(whoami)}"
chown -R "${DEPLOY_USER}:${DEPLOY_USER}" "$CUSTOMER_DIR"
echo "[onboard] Set ownership of ${CUSTOMER_DIR} to ${DEPLOY_USER}"

# ──────────────────────────────────────────────────────────────────────
# 4. DNS step (manual, per Q5.a-2)
# ──────────────────────────────────────────────────────────────────────
ANDROS_PUBLIC_IP=$(curl -s --max-time 5 https://ifconfig.me || echo "<unknown — check ANDROS public IP manually>")
cat <<EOF

╔══════════════════════════════════════════════════════════════════╗
║ DNS RECORD REQUIRED — add manually in Cloudflare dashboard:      ║
║                                                                  ║
║   Zone:  isnex.eu                                                 ║
║   Type:  A                                                        ║
║   Name:  ${SLUG}                                                  ║
║   Value: ${ANDROS_PUBLIC_IP}                                      ║
║   Proxy: Proxied (orange cloud)                                   ║
║   TTL:   Auto                                                     ║
║                                                                  ║
║ Final URL: https://${DOMAIN}                                      ║
╚══════════════════════════════════════════════════════════════════╝

EOF
if [[ "$SKIP_DNS_PROMPT" -eq 0 ]]; then
    read -rp "[onboard] Press ENTER after the DNS record is created (or Ctrl+C to abort)..."
else
    echo "[onboard] --skip-dns-prompt set; assuming DNS record exists"
fi

# ──────────────────────────────────────────────────────────────────────
# 5. Issue per-customer LE cert via DNS-01 challenge
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Requesting Let's Encrypt cert for ${DOMAIN} (DNS-01)..."
sudo certbot certonly \
    --dns-cloudflare \
    --dns-cloudflare-credentials "${CF_CREDENTIALS}" \
    -d "${DOMAIN}" \
    --agree-tos \
    --non-interactive \
    -m "${CERT_EMAIL}" \
    --keep-until-expiring

if [[ ! -f "/etc/letsencrypt/live/${DOMAIN}/fullchain.pem" ]]; then
    echo "ERROR: cert request failed — check certbot logs" >&2
    exit 1
fi
echo "[onboard] Cert issued at /etc/letsencrypt/live/${DOMAIN}/"

# ──────────────────────────────────────────────────────────────────────
# 6. Install nginx config + reload
# ──────────────────────────────────────────────────────────────────────
sudo cp "${SLUG}.nginx.conf" "${NGINX_CONF_DIR}/${SLUG}.conf"
sudo nginx -t
sudo systemctl reload nginx
echo "[onboard] nginx config installed at ${NGINX_CONF_DIR}/${SLUG}.conf"

# ──────────────────────────────────────────────────────────────────────
# 7. Start customer stack
# ──────────────────────────────────────────────────────────────────────
docker compose up -d
echo "[onboard] Containers starting; waiting for postgres healthcheck..."
for i in $(seq 1 30); do
    HEALTH=$(docker inspect --format '{{.State.Health.Status}}' "${SLUG}-postgres" 2>/dev/null || echo "starting")
    [[ "$HEALTH" == "healthy" ]] && break
    sleep 2
done
[[ "$HEALTH" != "healthy" ]] && { echo "ERROR: postgres did not become healthy"; exit 1; }

# ──────────────────────────────────────────────────────────────────────
# 7b. Wire customer into shared monitoring stack (idempotent)
# ──────────────────────────────────────────────────────────────────────
PROM_CONTAINER="${PROM_CONTAINER:-nex-prometheus}"
PROM_CONFIG="${PROM_CONFIG:-/opt/nex-automat/prometheus/prometheus.yml}"

if docker ps --format '{{.Names}}' | grep -q "^${PROM_CONTAINER}$"; then
    # 7b.1 Connect prometheus to customer's docker network so it can DNS-resolve
    # ${SLUG}-postgres-exporter (idempotent — 'already exists' is fine).
    docker network connect "${SLUG}-net" "${PROM_CONTAINER}" 2>/dev/null \
        && echo "[onboard] Connected ${PROM_CONTAINER} to ${SLUG}-net" \
        || echo "[onboard] ${PROM_CONTAINER} already on ${SLUG}-net (OK)"

    # 7b.2 Append scrape jobs (postgres-exporter + blackbox HTTP probe)
    # for this customer. Skip if already present (idempotent).
    PROM_DIRTY=0
    if [[ -w "${PROM_CONFIG}" ]]; then
        if ! grep -q "job_name: 'customer-${SLUG}-postgres'" "${PROM_CONFIG}"; then
            cat >> "${PROM_CONFIG}" <<EOF

  # Auto-added by onboard-customer.sh for customer '${SLUG}'
  - job_name: 'customer-${SLUG}-postgres'
    static_configs:
      - targets: ['${SLUG}-postgres-exporter:9187']
        labels:
          customer: '${SLUG}'
EOF
            echo "[onboard] Added scrape job customer-${SLUG}-postgres"
            PROM_DIRTY=1
        fi
        if ! grep -q "job_name: 'blackbox-customer-${SLUG}'" "${PROM_CONFIG}"; then
            cat >> "${PROM_CONFIG}" <<EOF

  # Blackbox HTTP probe for customer '${SLUG}'
  - job_name: 'blackbox-customer-${SLUG}'
    metrics_path: /probe
    params:
      module: [http_2xx]
    static_configs:
      - targets: ['https://${DOMAIN}/']
        labels:
          customer: '${SLUG}'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: blackbox-exporter:9115
EOF
            echo "[onboard] Added scrape job blackbox-customer-${SLUG}"
            PROM_DIRTY=1
        fi
        if [[ "$PROM_DIRTY" -eq 1 ]]; then
            # Hot-reload via SIGHUP (no --web.enable-lifecycle requirement).
            docker kill -s HUP "${PROM_CONTAINER}" >/dev/null && echo "[onboard] Reloaded ${PROM_CONTAINER}"
        else
            echo "[onboard] Prometheus scrape jobs for ${SLUG} already present (OK)"
        fi
    else
        echo "[onboard] WARNING: ${PROM_CONFIG} not writable — add scrape jobs manually"
    fi
else
    echo "[onboard] NOTE: ${PROM_CONTAINER} not running — skipping monitoring wire-up"
fi

# ──────────────────────────────────────────────────────────────────────
# 8. Apply migrations 001-016 (initial schema + seed)
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Applying migrations..."
for migration in "${MIGRATIONS_DIR}"/*.sql; do
    fname=$(basename "$migration")
    echo "[onboard]   - ${fname}"
    docker exec -i "${SLUG}-postgres" psql -U postgres -d nex_automat -q < "$migration" >/dev/null
done

# ──────────────────────────────────────────────────────────────────────
# 9. Admin credentials — admin/admin from migration 002 seed
#    Director logs in immediately, changes password via UI, creates users.
# ──────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────
# 10. Healthcheck via public URL
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Verifying public URL..."
sleep 3
HEALTH_URL="https://${DOMAIN}/health"
for i in $(seq 1 15); do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$HEALTH_URL" || echo "000")
    [[ "$STATUS" == "200" ]] && break
    sleep 2
done
if [[ "$STATUS" != "200" ]]; then
    echo "WARNING: ${HEALTH_URL} returned HTTP ${STATUS} (expected 200)"
    echo "Check: nginx config, container logs, Cloudflare DNS propagation"
fi

# ──────────────────────────────────────────────────────────────────────
# 11. Summary
# ──────────────────────────────────────────────────────────────────────
cat <<EOF

╔══════════════════════════════════════════════════════════════════╗
║ Customer '${SLUG}' onboarded successfully                        ║
╠══════════════════════════════════════════════════════════════════╣
║ URL:            https://${DOMAIN}                                 ║
║ Health:         HTTP ${STATUS}                                    ║
║ Initial login:  admin / admin                                     ║
║                                                                  ║
║ NEXT STEPS:                                                       ║
║  1. Open URL in browser, login admin/admin                        ║
║  2. Immediately change admin password via UI                      ║
║     (System → Užívatelia → admin → Change password)              ║
║  3. Create customer users via UI (System → Užívatelia → Add)     ║
║  4. (Optional) Configure Cloudflare Access policy for ${DOMAIN}  ║
║     (Zero Trust → Access → Applications → Add)                   ║
║  5. (Optional) Run MIG module for NEX Genesis data import        ║
║                                                                  ║
║ Backups: configure cron via scripts/backup-customer.sh           ║
║ Cert renewal: certbot timer auto-renews 30 days before expiry    ║
╚══════════════════════════════════════════════════════════════════╝

EOF
