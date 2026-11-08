FROM python:3.11-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY application.py ./application.py

# Identifica que la aplicación se ejecuta dentro de una imagen Docker.
ENV DOCKER_ENV=true

# Railway usa PORT cuando lo define, de lo contrario el contenedor usa 5000.
EXPOSE 5000
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-5000} app.app:app"]
