# 1. Utiliser une image Python officielle légère
FROM python:3.12-slim

# 2. Définir des variables d'environnement pour optimiser Python dans Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Définir le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 4. Installer les dépendances système nécessaires pour Pillow (images)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copier le fichier requirements.txt et installer les dépendances Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copier tout le reste du code du projet dans le conteneur
COPY . /app/

# 7. Exposer le port 8000
EXPOSE 8000

# 8. Commande par défaut pour appliquer les migrations et lancer le serveur
CMD python manage.py migrate && python manage.py runserver 0.0.0.0:8000