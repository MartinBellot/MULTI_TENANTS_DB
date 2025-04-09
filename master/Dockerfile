# Utilisation d'une image officielle de Python
FROM python:3.10-slim

# Empêcher la création de fichiers .pyc et d'autres caches
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Répertoire de travail dans le container
WORKDIR /app

# Copier le fichier des dépendances et installer les modules
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans le container
COPY . /app/

# Collecte des fichiers statiques (si applicable)
RUN python manage.py collectstatic --noinput

# Exposer le port utilisé par l'application
EXPOSE 8000

# Commande de démarrage avec Gunicorn
CMD ["gunicorn", "master.wsgi:application", "--bind", "0.0.0.0:8000"]