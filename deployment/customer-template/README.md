# Customer deployment template

This directory holds template files used by `scripts/onboard-customer.sh` to
provision a fully isolated NEX Manager stack per customer (per Phase D
architecture; see KB DECISIONS.md D-024).

## Files

| File | Purpose |
|---|---|
| `docker-compose.yml.template` | Per-customer compose stack — postgres + backend + frontend, dedicated Docker network, no host port exposure |
| `.env.example` | Sample env file with required variables; onboard script generates random secrets |
| `nginx-snippet.conf.template` | Host nginx server block routing `<slug>.nex-automat.isnex.eu` → frontend container |

## How a customer gets onboarded

```bash
cd /opt/nex-automat-src
sudo ./scripts/onboard-customer.sh <slug>
```

Script does:
1. Validate slug (lowercase, 3-15 chars, not yet used)
2. Create `/opt/customers/<slug>/`
3. Copy templates and substitute `${SLUG}` variable
4. Generate random `POSTGRES_PASSWORD` + `JWT_SECRET_KEY` into `.env`
5. Print Cloudflare DNS record to add manually (per Q5.a-2)
6. Wait for ENTER after DNS confirmed
7. Install nginx config, reload nginx
8. `docker compose up -d` (postgres + backend + frontend)
9. Apply DB migrations 001-016
10. Seed admin user with random password (per Q5.c-2), print to console
11. Healthcheck `https://<slug>.nex-automat.isnex.eu/health`

## After onboarding

- Set up Cloudflare Access policy in Zero Trust dashboard for this subdomain
- Predaj initial admin password customerovi cez secure channel
- Customer logs in, immediately changes password
- (Optional) Run MIG module to import historical data from NEX Genesis Btrieve

## Migrating customer to self-hosted server

Each customer's stack is fully self-contained:

```bash
# On ANDROS:
./scripts/backup-customer.sh <slug>
# Produces /opt/backups/<slug>/<slug>-<date>.tgz

# Transfer to customer server, then:
tar xzf <slug>-<date>.tgz -C /opt/customers/<slug>/
cd /opt/customers/<slug>
docker compose up -d
docker exec <slug>-postgres psql -U postgres < db.sql
# Update DNS to point <slug>.nex-automat.isnex.eu → customer's IP
```

No code changes required — customer server runs the same images.
