FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default tenant (override via docker-compose or -e)
ENV WORKER_TENANT=supplier

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install centralized config package
COPY packages/nex-config/ /tmp/nex-config/
RUN pip install --no-cache-dir /tmp/nex-config/ && rm -rf /tmp/nex-config/

# Install shared invoice worker package
COPY packages/nex-invoice-worker/ /tmp/nex-invoice-worker/
RUN pip install --no-cache-dir /tmp/nex-invoice-worker/ && rm -rf /tmp/nex-invoice-worker/

# Copy requirements and install remaining dependencies
COPY packages/nex-invoice-worker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Default command - run main worker
CMD ["python", "-m", "nex_invoice_worker.workers.main_worker"]
