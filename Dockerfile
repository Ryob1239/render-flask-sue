FROM python:3.10-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variable inyectada para identificar el entorno Docker
ENV DOCKER_ENV=true

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.app:app"]