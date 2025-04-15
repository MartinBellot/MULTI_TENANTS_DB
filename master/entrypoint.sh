#!/bin/sh
set -e

ENV_FILE=".env"

generate_secret_key() {
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
}

echo "=== Checking DJANGO_SECRET_KEY ==="
CURRENT_SECRET=$(grep "^DJANGO_SECRET_KEY=" "$ENV_FILE" | cut -d '=' -f2-)

if [ -z "$CURRENT_SECRET" ]; then
    echo "DJANGO_SECRET_KEY is missing or empty, generating one..."
    GENERATED_SECRET_KEY=$(generate_secret_key)

    # Supprime la ligne vide si elle existe déjà
    sed -i '/^DJANGO_SECRET_KEY=/d' "$ENV_FILE"

    echo "DJANGO_SECRET_KEY=$GENERATED_SECRET_KEY" >> "$ENV_FILE"
    export DJANGO_SECRET_KEY="$GENERATED_SECRET_KEY"
else
    export DJANGO_SECRET_KEY="$CURRENT_SECRET"
fi

# Recharge la clé pour l’environnement actuel
export DJANGO_SECRET_KEY=$(grep "^DJANGO_SECRET_KEY=" "$ENV_FILE" | cut -d '=' -f2-)

echo "Waiting for database at $DB_HOST:$DB_PORT..."
while ! nc -z $DB_HOST $DB_PORT; do
  echo "Database not ready, waiting..."
  sleep 1
done
echo "Database is ready!"

ls -l /app

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