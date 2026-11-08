# Corrección del despliegue multientorno: Render y Railway

## Diagnóstico de los logs del 7 de noviembre de 2026

**GitHub Actions:** Pruebas, Docker Hub, Render (notificación) y Azure salen en verde; Railway falla con `Service not found`.

**Render:** La instalación fue exitosa pero el servidor falló porque el comando configurado en Render es `gunicorn app:app`. El paquete `app/__init__.py` no exportaba una variable Flask denominada `app`.

**Railway:** Ocurrieron DOS problemas distintos:

1. **En GitHub Actions:** `Service not found` indica que Railway CLI no encuentra el servicio en el proyecto/entorno al que tiene acceso el token. Hay que comprobar los IDs y el alcance del token. **Este problema no se corrige solo cambiando código Python**.
2. **En los registros del contenedor:** `Failed to find attribute 'app' in 'app'` es el mismo problema de punto de entrada que en Render. Se resuelve exportando el objeto Flask desde `app/__init__.py` y actualizando el despliegue.

## Archivos que se corrigieron

- `app/__init__.py`: exporta el objeto Flask (`from .app import app`). Así funcionan **ambas** rutas Gunicorn: `app:app` y `app.app:app`.
- `Dockerfile`: Python 3.11, punto de entrada `app.app:app`, enlace al puerto `${PORT:-5000}`.
- `render.yaml`: blueprint para runtime Python, con `gunicorn app.app:app --bind 0.0.0.0:$PORT`. No cambia automáticamente un servicio de Render ya creado manualmente.
- `.python-version`: usa Python 3.11 también en Render.
- `.github/workflows/ci-cd.yml`: Railway espera al resultado del despliegue y muestra una indicación más clara en caso de `Service not found`.
- `test/test_wsgi_import.py`: comprueba que ambos importadores WSGI exportan la misma instancia Flask.

## Pasos en Render

1. Confirma que el servicio corresponde a este repositorio y a la rama `main`.
2. En **Settings**, en **Build & Deploy** (el nombre exacto puede variar), cambia **Start Command** a `gunicorn app.app:app --bind 0.0.0.0:$PORT` si sigue siendo `gunicorn app:app`. La modificación de `app/__init__.py` permite también el comando anterior.
3. Haz commit de la corrección a `main`, despliega de nuevo y revisa **Deploy Logs**: debe aparecer que Gunicorn inicia sin `AppImportError`.
4. Prueba la URL pública y verifica que responde la página. **GitHub Actions verde solo significa que el Deploy Hook aceptó la solicitud**, no que la nueva versión ya está funcionando.

## Pasos en Railway — importante

1. Abre el proyecto Railway que contiene el servicio Flask. En la paleta `Ctrl + K`, copia **Project ID**. Hazlo en el proyecto correcto.
2. Selecciona el servicio Flask dentro de ese proyecto. Con `Ctrl + K`, copia **Service ID** de ESE servicio. No es **Deployment ID** ni **Environment ID**.
3. En **Project Settings > Tokens**, confirma que el `RAILWAY_TOKEN` es un **Project Token**, generado para **ese mismo proyecto y el entorno `production`**. Si es de otro proyecto o entorno, crea uno nuevo y sustituye el Secret (no compartas el token).
4. En GitHub > repositorio > Settings > Secrets and variables > Actions, comprueba los valores de `RAILWAY_PROJECT_ID`, `RAILWAY_SERVICE_ID` (pueden estar en Secrets o Variables) y `RAILWAY_TOKEN` (en Secrets). Usa el icono de lápiz para reemplazar los IDs si estaban equivocados.
5. Si tu entorno no se llama `production`, crea una Variable `RAILWAY_ENVIRONMENT` con el nombre correcto, por ejemplo `staging`, y asegúrate de que el token corresponde a ese entorno.
6. En **Service > Settings > Deploy**, si existe un **Custom Start Command** viejo `gunicorn app:app`, puedes cambiarlo a `gunicorn --bind 0.0.0.0:$PORT app.app:app` (la nueva exportación también soporta `app:app`). La construcción con Dockerfile dispone de un CMD que respeta `PORT`.
7. Confirma que los nuevos archivos están en `main` y vuelve a ejecutar el flujo GitHub Actions. El pipeline **no puede reparar un Service ID de Railway que pertenezca a otro proyecto**.

## Verificación después del commit

En GitHub Actions deben pasar las pruebas y los cuatro trabajos. Después revisa que Render y Railway tengan realmente un despliegue **Live / Healthy** y abre sus URLs públicas.

En Azure `dcazure` se mantiene el despliegue Python existente. No cambies los Secrets que ya funcionan.
