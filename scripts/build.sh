#!/usr/bin/env bash
# Exit on error
set -e

# Install Python deps
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "from django.contrib.auth.models import User; \
u='Anirban'; \
e='bandyopadhyay4u@gmail.com'; \
p='EduCollab#123'; \
from django.db import IntegrityError; \
try: \
    User.objects.create_superuser(u, e, p); \
    print('✅ Superuser created successfully'); \
except IntegrityError: \
    print('⚠️ Superuser already exists'); \
except Exception as err: \
    print('⚠️ Error creating superuser:', err)" | python manage.py shell
