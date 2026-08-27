#!/bin/sh
set -e

echo "==> Starting WIN PROFESSIONAL ACADEMY entrypoint..."

# Apply database migrations
echo "==> Applying database migrations..."
python manage.py migrate --no-input

# Seed database with initial academy profile & courses if empty
echo "==> Checking and seeding database records..."
python manage.py seed_academy_data

# Create superuser automatically if environment variables are provided
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "==> Creating default superuser..."
    python manage.py createsuperuser --no-input || true
fi

echo "==> Starting Gunicorn web server..."
exec "$@"
