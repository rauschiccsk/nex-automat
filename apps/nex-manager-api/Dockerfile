FROM python:3.12-slim

WORKDIR /app

# Install nex-config package (centralized configuration)
COPY packages/nex-config/ /tmp/nex-config/
RUN pip install --no-cache-dir /tmp/nex-config/ && rm -rf /tmp/nex-config/

# Install dependencies
COPY apps/nex-manager-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY apps/nex-manager-api/ .

# Copy module registry (YAML — single source of truth for modules)
COPY module_registry.yaml /app/module_registry.yaml

# Copy nex-migration modules (needed by migration router for PAB run)
# router.py resolves: Path(__file__).parents[2] / "nex-migration" → /nex-migration
COPY apps/nex-migration/config/ /nex-migration/config/
COPY apps/nex-migration/transform/ /nex-migration/transform/
COPY apps/nex-migration/load/ /nex-migration/load/
COPY apps/nex-migration/data/ /nex-migration/data/
COPY apps/nex-migration/__init__.py /nex-migration/__init__.py

EXPOSE 9110

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9110", "--log-level", "info", "--access-log"]
