FROM python:3.10-slim

# Installer l'outil ping (iputils-ping)
RUN apt-get update \
	&& apt-get install -y --no-install-recommends iputils-ping \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5002
CMD ["python", "app.py"]
