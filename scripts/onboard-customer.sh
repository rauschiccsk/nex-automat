#!/usr/bin/env bash
#
# onboard-customer.sh — provision a fully isolated NEX Manager stack
#                       for a new customer on ANDROS.
#
# Usage:  sudo ./scripts/onboard-customer.sh <slug>
#
# See KB DECISIONS.md D-024 + deployment/customer-template/README.md
# for architecture context.
#
# Prerequisites on ANDROS:
#   - Docker + docker compose v2
#   - nginx with wildcard cert *.nex-automat.isnex.eu installed
#   - Docker network 'nex-proxy-net' created (one-time setup)
#   - Migrations 001-016 available at /opt/nex-automat-src/database/migrations/
#   - nex-manager-backend:latest + nex-manager-frontend:latest images available

set -euo pipefail

SLUG="${1:-}"
REPO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
TEMPLATE_DIR="${REPO_ROOT}/deployment/customer-template"
MIGRATIONS_DIR="${REPO_ROOT}/database/migrations"
CUSTOMERS_ROOT="${CUSTOMERS_ROOT:-/opt/customers}"
NGINX_CONF_DIR="${NGINX_CONF_DIR:-/etc/nginx/conf.d}"

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
CUSTOMER_DIR="${CUSTOMERS_ROOT}/${SLUG}"
if [[ -d "$CUSTOMER_DIR" ]]; then
    echo "ERROR: ${CUSTOMER_DIR} already exists — refusing to overwrite" >&2
    exit 1
fi
if docker ps -a --format '{{.Names}}' | grep -qE "^${SLUG}-(postgres|backend|frontend)$"; then
    echo "ERROR: containers ${SLUG}-* already exist — clean up first" >&2
    exit 1
fi

echo "[onboard] Provisioning customer '${SLUG}'"

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

# .env file
cat > .env <<EOF
SLUG=${SLUG}
IMAGE_TAG=latest
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
JWT_SECRET_KEY=${JWT_SECRET_KEY}
EOF
chmod 600 .env

# docker-compose.yml — straight copy (uses ${VAR} interpolation from .env)
cp "${TEMPLATE_DIR}/docker-compose.yml.template" docker-compose.yml

# nginx snippet — render ${SLUG} substitutions
SLUG="${SLUG}" envsubst '${SLUG}' \
    < "${TEMPLATE_DIR}/nginx-snippet.conf.template" \
    > "${SLUG}.nginx.conf"

echo "[onboard] Generated ${CUSTOMER_DIR}/.env, docker-compose.yml, ${SLUG}.nginx.conf"

# ──────────────────────────────────────────────────────────────────────
# 4. DNS step (manual, per Q5.a-2)
# ──────────────────────────────────────────────────────────────────────
ANDROS_PUBLIC_IP=$(cat "${CUSTOMER_DIR}/../.andros-public-ip" 2>/dev/null || echo "<see /opt/customers/.andros-public-ip>")
cat <<EOF

╔══════════════════════════════════════════════════════════════════╗
║ DNS RECORD REQUIRED — add manually in Cloudflare dashboard:      ║
║                                                                  ║
║   Type:  A                                                        ║
║   Name:  ${SLUG}.nex-automat                                      ║
║   Value: ${ANDROS_PUBLIC_IP}                                      ║
║   Proxy: Enabled (orange cloud)                                   ║
║   TTL:   Auto                                                     ║
║                                                                  ║
║ Domain: isnex.eu                                                  ║
║ Final URL: https://${SLUG}.nex-automat.isnex.eu                  ║
╚══════════════════════════════════════════════════════════════════╝

EOF
read -rp "[onboard] Press ENTER after the DNS record is created (or Ctrl+C to abort)..."

# ──────────────────────────────────────────────────────────────────────
# 5. Install nginx config + reload
# ──────────────────────────────────────────────────────────────────────
cp "${SLUG}.nginx.conf" "${NGINX_CONF_DIR}/${SLUG}.conf"
nginx -t
systemctl reload nginx
echo "[onboard] nginx config installed at ${NGINX_CONF_DIR}/${SLUG}.conf and reloaded"

# ──────────────────────────────────────────────────────────────────────
# 6. Start customer stack
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
# 7. Apply migrations 001-016 (initial schema + seed)
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Applying migrations..."
for migration in "${MIGRATIONS_DIR}"/*.sql; do
    fname=$(basename "$migration")
    echo "[onboard]   - ${fname}"
    docker exec -i "${SLUG}-postgres" psql -U postgres -d nex_automat -q < "$migration" >/dev/null
done

# ──────────────────────────────────────────────────────────────────────
# 8. Set initial admin password (overwrite seed default)
# ──────────────────────────────────────────────────────────────────────
ADMIN_HASH=$(docker run --rm python:3.12-alpine sh -c \
    "pip install -q bcrypt && python -c \"import bcrypt; print(bcrypt.hashpw('${ADMIN_PASSWORD}'.encode()[:72], bcrypt.gensalt()).decode())\"")
docker exec -i "${SLUG}-postgres" psql -U postgres -d nex_automat -q \
    -c "UPDATE users SET password_hash='${ADMIN_HASH}' WHERE login_name='admin'"

# ──────────────────────────────────────────────────────────────────────
# 9. Healthcheck via public URL (DNS + cert + nginx + container)
# ──────────────────────────────────────────────────────────────────────
echo "[onboard] Verifying public URL..."
sleep 3
HEALTH_URL="https://${SLUG}.nex-automat.isnex.eu/health"
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
# 10. Summary
# ──────────────────────────────────────────────────────────────────────
cat <<EOF

╔══════════════════════════════════════════════════════════════════╗
║ Customer '${SLUG}' onboarded successfully                        ║
╠══════════════════════════════════════════════════════════════════╣
║ URL:            https://${SLUG}.nex-automat.isnex.eu             ║
║ Health:         HTTP ${STATUS}                                    ║
║ Admin login:    admin                                             ║
║ Admin password: ${ADMIN_PASSWORD}                                 ║
║                                                                  ║
║ NEXT STEPS (manual):                                              ║
║  1. Configure Cloudflare Access policy for this subdomain        ║
║     (Zero Trust → Access → Applications → Add)                   ║
║  2. Deliver admin password to customer via SECURE channel        ║
║     (Vaultwarden share / encrypted email — NOT this terminal)    ║
║  3. Customer logs in, immediately changes password               ║
║  4. (Optional) Run MIG module for historical data import         ║
║                                                                  ║
║ Backups: configure cron via scripts/backup-customer.sh           ║
╚══════════════════════════════════════════════════════════════════╝

EOF
