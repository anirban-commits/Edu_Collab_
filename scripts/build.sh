#!/usr/bin/env bash
# Exit on error
set -e

# Install Python deps
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate