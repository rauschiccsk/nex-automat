# ANDROS Monitoring Setup

**Dátum:** 2026-01-16  
**Server:** Dell PowerEdge R740XD (192.168.100.23 / 100.107.134.104)  
**Session:** Prometheus + Grafana + Alertmanager

---

## Prehľad komponentov

| Služba | Container | Port | Image |
|--------|-----------|------|-------|
| Prometheus | nex-prometheus | 9090 | prom/prometheus:latest |
| Grafana | nex-grafana | 3000 | grafana/grafana:latest |
| Alertmanager | nex-alertmanager | 9093 | prom/alertmanager:latest |
| Node Exporter | nex-node-exporter | 9100 | prom/node-exporter:latest |
| cAdvisor | nex-cadvisor | 8081 | gcr.io/cadvisor/cadvisor:latest |
| Postgres Exporter | nex-postgres-exporter | 9187 | prometheuscommunity/postgres-exporter:latest |

---

## Konfiguračné súbory

### docker-compose.monitoring.yml

Umiestnenie: `/opt/nex-automat/docker-compose.monitoring.yml`

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: nex-prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./prometheus/rules.yml:/etc/prometheus/rules.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.enable-lifecycle'
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana:latest
    container_name: nex-grafana
    restart: unless-stopped
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning:ro
    ports:
      - "3000:3000"
    depends_on:
      - prometheus

  node-exporter:
    image: prom/node-exporter:latest
    container_name: nex-node-exporter
    restart: unless-stopped
    command:
      - '--path.rootfs=/host'
    volumes:
      - '/:/host:ro,rslave'
    ports:
      - "9100:9100"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: nex-cadvisor
    restart: unless-stopped
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    ports:
      - "8081:8080"

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:latest
    container_name: nex-postgres-exporter
    restart: unless-stopped
    environment:
      - DATA_SOURCE_NAME=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}?sslmode=disable
    ports:
      - "9187:9187"
    depends_on:
      - postgres

  alertmanager:
    image: prom/alertmanager:latest
    container_name: nex-alertmanager
    restart: unless-stopped
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml:ro
      - alertmanager_data:/alertmanager
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    ports:
      - "9093:9093"

volumes:
  alertmanager_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/alertmanager
  prometheus_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/prometheus
  grafana_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data/docker-volumes/grafana
```

### prometheus/prometheus.yml

Umiestnenie: `/opt/nex-automat/prometheus/prometheus.yml`

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

rule_files:
  - '/etc/prometheus/rules.yml'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
```

### prometheus/rules.yml

Umiestnenie: `/opt/nex-automat/prometheus/rules.yml`

```yaml
groups:
  - name: node_alerts
    rules:
      - alert: HighCpuUsage
        expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: "CPU usage is above 80% for 5 minutes (current: {{ $value | printf \"%.1f\" }}%)"

      - alert: HighMemoryUsage
        expr: (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: "Memory usage is above 85% (current: {{ $value | printf \"%.1f\" }}%)"

      - alert: DiskSpaceLow
        expr: (1 - (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"})) * 100 > 85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: "Disk usage is above 85% on {{ $labels.mountpoint }}"

      - alert: DiskSpaceCritical
        expr: (1 - (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes{fstype!="tmpfs"})) * 100 > 95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Critical disk space on {{ $labels.instance }}"
          description: "Disk usage is above 95% on {{ $labels.mountpoint }}"

  - name: container_alerts
    rules:
      - alert: ContainerRestarting
        expr: increase(container_start_time_seconds{name=~"nex-.*"}[5m]) > 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Container {{ $labels.name }} is restarting"
          description: "Container {{ $labels.name }} has restarted multiple times"

      - alert: ContainerHighCpu
        expr: rate(container_cpu_usage_seconds_total{name=~"nex-.*"}[5m]) * 100 > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU in container {{ $labels.name }}"
          description: "Container {{ $labels.name }} CPU usage is above 80%"

      - alert: ContainerHighMemory
        expr: (container_memory_usage_bytes{name=~"nex-.*"} / container_spec_memory_limit_bytes{name=~"nex-.*"} * 100 > 85) and container_spec_memory_limit_bytes{name=~"nex-.*"} > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory in container {{ $labels.name }}"
          description: "Container {{ $labels.name }} memory usage is above 85%"

  - name: postgres_alerts
    rules:
      - alert: PostgresDown
        expr: pg_up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "PostgreSQL is down"
          description: "PostgreSQL database is not responding"

      - alert: PostgresTooManyConnections
        expr: pg_stat_activity_count > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "PostgreSQL too many connections"
          description: "PostgreSQL has {{ $value }} active connections"
```

### alertmanager/alertmanager.yml

Umiestnenie: `/opt/nex-automat/alertmanager/alertmanager.yml`

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'telegram-admin'

receivers:
  - name: 'telegram-admin'
    telegram_configs:
      - bot_token: '<TELEGRAM_ADMIN_BOT_TOKEN>'
        chat_id: <TELEGRAM_ADMIN_USER_ID>
        parse_mode: 'HTML'
        message: |
          🚨 <b>{{ .Status | toUpper }}</b>
          <b>Alert:</b> {{ .CommonAnnotations.summary }}
          <b>Severity:</b> {{ .CommonLabels.severity }}
          <b>Description:</b> {{ .CommonAnnotations.description }}

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname']
```

### grafana/provisioning/datasources/prometheus.yml

Umiestnenie: `/opt/nex-automat/grafana/provisioning/datasources/prometheus.yml`

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
```

---

## Adresárová štruktúra

```
/opt/nex-automat/
├── docker-compose.yml
├── docker-compose.monitoring.yml
├── .env
├── prometheus/
│   ├── prometheus.yml
│   └── rules.yml
├── alertmanager/
│   └── alertmanager.yml
└── grafana/
    └── provisioning/
        └── datasources/
            └── prometheus.yml

/data/docker-volumes/
├── prometheus/
├── grafana/
└── alertmanager/
```

---

## Grafana Dashboardy

| Dashboard | Grafana ID | Účel |
|-----------|------------|------|
| Node Exporter Full | 1860 | Systémové metriky (CPU, RAM, Disk, Network) |
| cAdvisor Exporter | 14282 | Docker kontajner metriky |
| PostgreSQL Database | 9628 | PostgreSQL metriky |

Import: Dashboards → New → Import → zadaj ID → Load → vyber Prometheus → Import

---

## Prístupy

| Služba | URL | Credentials |
|--------|-----|-------------|
| Grafana | http://192.168.100.23:3000 | admin / Andros-2026 |
| Prometheus | http://192.168.100.23:9090 | - |
| Alertmanager | http://192.168.100.23:9093 | - |

---

## Užitočné príkazy

```bash
# Spustenie stacku
cd /opt/nex-automat
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d

# Stav služieb
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml ps

# Reload Prometheus konfigurácie
curl -X POST http://127.0.0.1:9090/-/reload

# Aktívne alerty
curl -s http://127.0.0.1:9090/api/v1/alerts | jq '.data.alerts[] | {alert: .labels.alertname, state: .state}'

# Prometheus targets
curl -s http://127.0.0.1:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Test Telegram notifikácie
curl -X POST http://127.0.0.1:9093/api/v2/alerts \
  -H "Content-Type: application/json" \
  -d '[{"labels":{"alertname":"Test","severity":"warning"},"annotations":{"summary":"Test notification","description":"Test from ANDROS"}}]'

# Logy
docker logs nex-prometheus --tail 50
docker logs nex-alertmanager --tail 50
docker logs nex-grafana --tail 50
```

---

## Riešené problémy

1. **Network nex-network not found** - monitoring services používajú default network, nie explicitný nex-network

2. **Grafana redirect na Tailscale IP** - odstránené GF_SERVER_ROOT_URL a GF_SERVER_SERVE_FROM_SUB_PATH

3. **Alertmanager env variables** - Alertmanager nepodporuje ${VAR} syntax, nutné hardcoded hodnoty

4. **Postgres exporter authentication** - použiť ${POSTGRES_USER} nie "postgres"

5. **ContainerHighMemory false alerts** - pridaná podmienka `container_spec_memory_limit_bytes > 0`