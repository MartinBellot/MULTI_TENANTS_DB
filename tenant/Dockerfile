# Utilisation d'une image officielle de Python avec un tag spécifique
FROM python:3.10.12-slim-bullseye

# Empêcher la création de fichiers .pyc et d'autres caches
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Installer netcat pour le wait-for-db
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Répertoire de travail dans le container
WORKDIR /app

# Copier le fichier des dépendances et installer les modules
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans le container
COPY . /app/

# Copier le script entrypoint dans le container et le rendre exécutable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Exposer le port utilisé par l'application
EXPOSE 8001

# Utiliser entrypoint.sh comme point d'entrée
ENTRYPOINT ["/app/entrypoint.sh"]