FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY activities/ ./activities/
COPY adapters/ ./adapters/
COPY config/ ./config/
COPY converters/ ./converters/
COPY models/ ./models/
COPY scheduler/ ./scheduler/
COPY workers/ ./workers/
COPY workflows/ ./workflows/
COPY __init__.py .

# Default command - run main worker
CMD ["python", "-m", "workers.main_worker"]
