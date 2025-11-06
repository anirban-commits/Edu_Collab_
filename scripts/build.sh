#!/usr/bin/env bash
# Exit on error
set -e

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Create superuser safely (one-liner)
python manage.py shell <<EOF
from django.contrib.auth.models import User
username = "Anirban"
email = "bandyopadhyay4u@gmail.com"
password = "EduCollab#123"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superuser created successfully")
else:
    print("⚠️ Superuser already exists")
EOF
