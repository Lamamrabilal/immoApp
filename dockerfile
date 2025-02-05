# Utiliser une image Python officielle comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans le répertoire de travail
COPY . .

# Expose le port 8000 pour Django
EXPOSE 8000


# Commande pour démarrer le serveur de développement Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]