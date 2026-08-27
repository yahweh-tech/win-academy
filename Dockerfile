# ==============================================================================
# WIN PROFESSIONAL ACADEMY - PRODUCTION DOCKERFILE
# ==============================================================================
FROM python:3.14-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PORT=8000

# Install system dependencies (build-essential for C extensions, libpq for PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Collect static files for production
RUN python manage.py collectstatic --no-input

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health/ || exit 1

# Make entrypoint script executable if present
RUN chmod +x /app/entrypoint.sh 2>/dev/null || true

# Run production server using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "config.wsgi:application"]
