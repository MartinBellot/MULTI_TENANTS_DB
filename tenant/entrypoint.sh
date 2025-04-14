#!/bin/sh
set -e

echo "Waiting for database at $DB_HOST:$DB_PORT..."
# Attendre que le service de base de données soit accessible
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Database not ready, waiting..."
  sleep 1
done
echo "Database is ready!"

echo "=== Migrating database ==="
python manage.py makemigrations
python manage.py migrate --noinput

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Creating superuser (if needed) ==="
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    print("Creating superuser...")
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )
else:
    print("Superuser already exists.")
EOF

echo "=== Starting Gunicorn ==="
exec gunicorn tenant.wsgi:application --bind 0.0.0.0:8001 --reload