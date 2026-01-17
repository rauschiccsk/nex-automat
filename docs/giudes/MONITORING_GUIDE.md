# ANDROS Monitoring - Používateľský návod

## Prístupy

| Služba | URL | Účel |
|--------|-----|------|
| Grafana | http://192.168.100.23:3000 | Vizualizácia a dashboardy |
| Prometheus | http://192.168.100.23:9090 | Metriky a query |
| Alertmanager | http://192.168.100.23:9093 | Správa alertov |

**Grafana login:** admin / Andros-2026

---

## Grafana - Denné používanie

### Ako zobraziť dashboard

1. Otvor http://192.168.100.23:3000
2. Ľavé menu → **Dashboards**
3. Vyber dashboard:
   - **Node Exporter Full** - CPU, RAM, Disk, Network servera
   - **cAdvisor Exporter** - Docker kontajnery
   - **PostgreSQL Database** - Databázové metriky

### Zmena časového rozsahu

- Vpravo hore klikni na "Last 6 hours"
- Vyber: Last 15 minutes, Last 1 hour, Last 24 hours, Last 7 days
- Alebo vlastný rozsah cez kalendár

### Auto-refresh

- Vpravo hore vedľa času je refresh ikona
- Nastav interval: 5s, 10s, 30s, 1m, 5m

### Čo sledovať denne

**Node Exporter Full:**
- CPU Busy < 80%
- RAM Used < 85%
- Disk Used < 85%
- Network Traffic - neobvyklé špičky

**cAdvisor:**
- Všetky nex-* kontajnery majú metriky
- Memory Usage - žiadny kontajner nekontrolovane rastie
- CPU Usage - žiadny kontajner nezaberá 100%

---

## Prometheus - Ad-hoc queries

### Užitočné query (zadaj do http://192.168.100.23:9090)

```promql
# CPU využitie servera (%)
100 - (avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# RAM využitie (%)
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100

# Disk využitie root partície (%)
(1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})) * 100

# Počet aktívnych PostgreSQL spojení
pg_stat_activity_count

# Memory použitie kontajnerov
container_memory_usage_bytes{name=~"nex-.*"}

# CPU rate kontajnerov
rate(container_cpu_usage_seconds_total{name=~"nex-.*"}[5m])
```

### Ako spustiť query

1. Otvor http://192.168.100.23:9090
2. Do poľa "Expression" vlož query
3. Klikni **Execute**
4. Prepni medzi **Table** a **Graph** view

---

## Alertmanager - Správa alertov

### Zobrazenie aktívnych alertov

- http://192.168.100.23:9093/#/alerts
- Alebo: `curl -s http://127.0.0.1:9093/api/v2/alerts | jq`

### Silence (dočasné stíšenie alertu)

1. Otvor http://192.168.100.23:9093
2. Pri alerte klikni **Silence**
3. Nastav dobu trvania (napr. 2h pre maintenance)
4. Pridaj komentár prečo

### Kedy dostaneš Telegram notifikáciu

- **FIRING** - keď alert začne (problém nastal)
- **RESOLVED** - keď sa problém vyriešil

---

## Troubleshooting

### Kontajner nebeží

```bash
# Zisti ktorý
docker ps -a --filter "name=nex-" --format "{{.Names}} {{.Status}}"

# Pozri logy
docker logs nex-<meno> --tail 50

# Reštartuj
docker restart nex-<meno>
```

### Vysoké CPU/RAM

```bash
# Top procesy
htop

# Docker stats
docker stats --no-stream
```

### Prometheus nescrapuje target

```bash
# Over targets
curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'
```

### Alertmanager neposiela notifikácie

```bash
# Test
curl -X POST http://127.0.0.1:9093/api/v2/alerts \
  -H "Content-Type: application/json" \
  -d '[{"labels":{"alertname":"Test"},"annotations":{"summary":"Test"}}]'

# Logy
docker logs nex-alertmanager --tail 20
```

---

## Rýchle príkazy (SSH)

```bash
# Stav všetkých služieb
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml ps

# Reštart monitoringu
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml restart prometheus grafana alertmanager

# Aktívne alerty
curl -s http://127.0.0.1:9090/api/v1/alerts | jq '.data.alerts[] | {alert: .labels.alertname, state: .state}'

# Reload Prometheus konfigurácie
curl -X POST http://127.0.0.1:9090/-/reload

# Disk space
df -h /data
```

---

## Kontakty pre alerty

Telegram notifikácie chodia na: **@ai_dev_automatin_bot** (Admin bot)
Chat ID: 7204918893