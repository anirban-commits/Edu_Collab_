#!/usr/bin/env bash
# Exit on error
set -e

# Install Python deps
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

echo "from django.contrib.auth.models import User; 
User.objects.filter(username='Anirban').exists() or 
User.objects.create_superuser('Anirban', 'bandyopadhyay4u@gmail.com', 'EduCollab#123')" | python manage.py shell
