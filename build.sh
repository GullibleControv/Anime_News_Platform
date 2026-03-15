#!/usr/bin/env bash
# =================================================================
# Build script for Render deployment
# =================================================================
# Render runs this script during each deploy
# =================================================================

set -o errexit  # Exit on error

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Build complete!"
