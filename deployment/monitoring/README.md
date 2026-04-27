# Monitoring stack — versioned snapshot

Mirror of the production monitoring config at `/opt/nex-automat/` on ANDROS.
Tracked here for disaster recovery, change review, and replication on a
fresh server.

## What's here

| Path | Purpose |
|---|---|
| `docker-compose.monitoring.yml` | Compose stack: Prometheus, Grafana, Alertmanager, blackbox/postgres/node exporters, cAdvisor |
| `prometheus/prometheus.yml` | Scrape config — auto-grown by `scripts/onboard-customer.sh` (one job per customer) |
| `prometheus/rules.yml` | Host + container alert rules (CPU, RAM, disk, container restart) |
| `prometheus/rules.customers.yml` | Per-customer alerts: SiteDown, SlowResponse, CertExpiringSoon, PostgresDown, HighConnections, BackendContainerDown |
| `blackbox/blackbox.yml` | HTTPS probe module config (http_2xx) |
| `grafana/provisioning/datasources/prometheus.yml` | Auto-provisioned Prometheus datasource |
| `grafana/provisioning/dashboards/customers.yml` | Dashboard provider config |
| `grafana/dashboards/customer-overview.json` | "NEX Manager — Customer Overview" dashboard with `$customer` dropdown |
| `alertmanager/alertmanager.yml.example` | Routing template (Telegram receiver) — **real config with secrets stays on /opt/nex-automat/ only** |

## Sync workflow

The on-disk config at `/opt/nex-automat/` is source of truth (mutated by
onboard script). The repo copy is a snapshot for review/DR.

**After changes on disk** (e.g. after onboarding a new customer):
```bash
cd /opt/nex-automat-src
cp /opt/nex-automat/prometheus/prometheus.yml         deployment/monitoring/prometheus/
cp /opt/nex-automat/prometheus/rules.customers.yml    deployment/monitoring/prometheus/
cp /opt/nex-automat/docker-compose.monitoring.yml     deployment/monitoring/
git add deployment/monitoring/ && git commit -m "ops(monitoring): sync from /opt/nex-automat/"
```

**Pushing changes from repo to disk** (e.g. editing a rule in the repo first):
```bash
cp deployment/monitoring/prometheus/rules.customers.yml /opt/nex-automat/prometheus/
docker kill -s HUP nex-prometheus  # hot reload
```

## Bootstrapping on a fresh server

For replicating the monitoring stack on a new ANDROS instance:

```bash
# 1. Copy non-secret files from repo
sudo mkdir -p /opt/nex-automat
sudo cp -r deployment/monitoring/* /opt/nex-automat/

# 2. Create alertmanager config with REAL secrets (not in repo)
sudo cp /opt/nex-automat/alertmanager/alertmanager.yml.example \
        /opt/nex-automat/alertmanager/alertmanager.yml
sudo nano /opt/nex-automat/alertmanager/alertmanager.yml  # fill bot_token + chat_id

# 3. Create data volumes (compose expects them at /data/docker-volumes/...)
sudo mkdir -p /data/docker-volumes/{prometheus,grafana,alertmanager}

# 4. Start stack
cd /opt/nex-automat
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

## What's NOT versioned

- `alertmanager/alertmanager.yml` (production — contains Telegram bot_token + chat_id)
- `.env` (Grafana admin password, postgres password)
- Volume data (Prometheus TSDB, Grafana DB, Alertmanager state)
