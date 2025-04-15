#!/bin/sh
set -e

ENV_FILE=".env"

generate_secret_key() {
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
}

# === GÉNÉRATION DE LA SECRET KEY AVANT TOUT ===
echo "=== Checking DJANGO_SECRET_KEY ==="
if ! grep -q "^DJANGO_SECRET_KEY=" "$ENV_FILE"; then
    echo "DJANGO_SECRET_KEY missing, generating one..."
    GENERATED_SECRET_KEY=$(generate_secret_key)
    echo "" >> "$ENV_FILE"
    echo "DJANGO_SECRET_KEY=$GENERATED_SECRET_KEY" >> "$ENV_FILE"
fi

# Recharge la clé pour l’environnement actuel
export DJANGO_SECRET_KEY=$(grep "^DJANGO_SECRET_KEY=" "$ENV_FILE" | cut -d '=' -f2-)

echo "Waiting for database at $DB_HOST:$DB_PORT..."
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
exec gunicorn master.wsgi:application --bind 0.0.0.0:8000 --reload