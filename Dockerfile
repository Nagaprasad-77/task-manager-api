# Use official slim Python base
FROM python:3.11-slim

# Avoid hitting apt cache issues (better reproduceable)
ENV DEBIAN_FRONTEND=noninteractive

# Create app directory
WORKDIR /app

# Install system dependencies needed for typical python packages
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy and install python deps early (cacheable)
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && pip install --no-cache-dir -r /app/requirements.txt

# Copy app code
COPY . /app

# Create non-root user (optional, but recommended)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Expose port for API
EXPOSE 8000

# By default run the API. For celery you will override the command in docker run or docker-compose.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
