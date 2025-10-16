FROM python:3.10-slim

# Installer PHP CLI pour exécuter des fichiers .php (volontairement pour le CTF)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends php-cli \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5001
CMD ["python", "app.py"]
