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
#   Admin password is NOT printed to stdout (security). It is written to
#   /opt/customers/<slug>/.initial-admin-password (chmod 600, root owner).
#   Read it via: sudo cat /opt/customers/<slug>/.initial-admin-password
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
ADMIN_PASSWORD=$(openssl rand -base64 16 | tr -d '=+/' | cut -c1-16)

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
EOF
chmod 600 .env

cp "${TEMPLATE_DIR}/docker-compose.yml.template" docker-compose.yml

SLUG="${SLUG}" envsubst '${SLUG}' \
    < "${TEMPLATE_DIR}/nginx-snippet.conf.template" \
    > "${SLUG}.nginx.conf"

echo "[onboard] Generated ${CUSTOMER_DIR}/.env, docker-compose.yml, ${SLUG}.nginx.conf"

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
# 8. Apply migrations 001-016 (initial schema + seed)
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Applying migrations..."
for migration in "${MIGRATIONS_DIR}"/*.sql; do
    fname=$(basename "$migration")
    echo "[onboard]   - ${fname}"
    docker exec -i "${SLUG}-postgres" psql -U postgres -d nex_automat -q < "$migration" >/dev/null
done

# ──────────────────────────────────────────────────────────────────────
# 9. Set initial admin password (overwrite seed default)
# ──────────────────────────────────────────────────────────────────────
ADMIN_HASH=$(docker run --rm python:3.12-alpine sh -c \
    "pip install -q bcrypt && python -c \"import bcrypt; print(bcrypt.hashpw('${ADMIN_PASSWORD}'.encode()[:72], bcrypt.gensalt()).decode())\"")
docker exec -i "${SLUG}-postgres" psql -U postgres -d nex_automat -q \
    -c "UPDATE users SET password_hash='${ADMIN_HASH}' WHERE login_name='admin'"

# Save admin password to chmod-600 file (NOT stdout — avoids credential
# exposure when script runs via remote terminal / CI / Claude session).
PWD_FILE="${CUSTOMER_DIR}/.initial-admin-password"
echo "${ADMIN_PASSWORD}" > "${PWD_FILE}"
chmod 600 "${PWD_FILE}"
chown root:root "${PWD_FILE}"

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
║ Admin login:    admin                                             ║
║ Admin password: <saved to file — NOT printed for security>        ║
║                                                                  ║
║ To retrieve admin password:                                       ║
║   sudo cat ${PWD_FILE}║
║                                                                  ║
║ NEXT STEPS (manual):                                              ║
║  1. Configure Cloudflare Access policy for ${DOMAIN}             ║
║     (Zero Trust → Access → Applications → Add)                   ║
║  2. Deliver admin password to customer via SECURE channel        ║
║     (Vaultwarden share / encrypted email — NOT plain text)       ║
║  3. Customer logs in, immediately changes password               ║
║  4. (Optional) Run MIG module for historical data import         ║
║                                                                  ║
║ Backups: configure cron via scripts/backup-customer.sh           ║
║ Cert renewal: certbot timer auto-renews 30 days before expiry    ║
╚══════════════════════════════════════════════════════════════════╝

EOF
