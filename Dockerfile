# [FIX] VULNÉRABILITÉ IMAGE DOCKER CORRIGÉE - Trivy passera au vert
# 1. Utilisation d'une image de base récente (Python 3.12 sur Debian Bookworm)
FROM python:3.12-slim-bookworm

WORKDIR /app

# 2. Mise à jour des paquets de l'OS pour éliminer les vulnérabilités Debian
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary :all: -r requirements.txt

COPY . .

# 3. Bonne pratique de sécurité : Ne pas exécuter l'application en mode "root"
RUN useradd -m appuser
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
