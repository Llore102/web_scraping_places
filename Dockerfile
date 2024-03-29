# Dockerfile

FROM python:3.8.16

WORKDIR /app

# Instala el cliente Docker
RUN apt-get update && \
    apt-get install -y docker.io

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .

# Agrega el comando necesario para ejecutar el servicio adicional y luego inicia la aplicación Python
CMD ["sh", "-c", "docker-compose -f docker-compose-v3.yml up -d && python app.py"]
