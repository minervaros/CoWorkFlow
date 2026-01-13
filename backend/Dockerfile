FROM python:3.10-slim
WORKDIR /app
# Instalamos dependencias del sistema para MySQL
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "run.py"]