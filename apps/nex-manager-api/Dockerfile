FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 9110

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9110", "--log-level", "info", "--access-log"]
