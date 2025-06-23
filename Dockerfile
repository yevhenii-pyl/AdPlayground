FROM python:3.11-slim

# Install system dependencies (for MySQL client + Cassandra + C extensions)
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    libffi-dev \
    libev-dev \
    libssl-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Default command (can be overridden)
CMD ["sh", "-c", "python scripts/utils/fix_events.py && python scripts/run_seeders.py"]