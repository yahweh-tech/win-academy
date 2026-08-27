#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "==> Upgrading pip and installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py migrate --no-input

echo "==> Seeding initial academy data..."
python manage.py seed_academy_data

echo "==> Build completed successfully!"
