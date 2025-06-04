# Dockerfile
FROM python:3.13-alpine

# Install system dependencies for MySQL client
RUN apk add --no-cache gcc musl-dev libffi-dev mariadb-dev

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Default command (overridable)
CMD ["sh", "-c", "python scripts/utils/fix_events.py && python scripts/run_seeders.py"]
