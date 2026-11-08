# Azure App Service — `dcazure`

La aplicación de Azure es **Linux / Python 3.11 / Código**, no una aplicación contenedorizada.

## Configuración indispensable en Azure Portal

1. Abre el App Service **dcazure**.
2. En **Configuración > Variables de entorno** (o **Configuración > Configuración de la aplicación**), agrega o actualiza:
   - Nombre: `SCM_DO_BUILD_DURING_DEPLOYMENT`
   - Valor: `true`
   - Guarda y acepta reiniciar el servicio si Azure lo solicita.
3. En **Configuración > Configuración general** (la ubicación puede cambiar según la interfaz), establece **Comando de inicio**:

   `gunicorn --bind=0.0.0.0 --timeout 600 application:app`

   Guarda la configuración. El archivo `application.py` de la raíz exporta la aplicación Flask de `app/app.py`.
4. Verifica que en GitHub (Settings > Secrets and variables > Actions) estén:
   - Variable `AZURE_WEBAPP_NAME` = `dcazure`.
   - Secret `AZURE_WEBAPP_PUBLISH_PROFILE` = contenido completo del perfil de publicación de **dcazure**.
5. Confirma que **SCM Basic Auth Publishing Credentials** estén habilitadas **si** utilizas un perfil de publicación. Esta autenticación es menos segura; OpenID Connect es preferible para una configuración de producción.
6. Revisa que no exista otro workflow de Azure generado automáticamente que esté desplegando simultáneamente a la misma aplicación.

## Qué hace el workflow corregido

- Ejecuta pruebas unitarias con Python 3.11.
- Despliega Azure directamente desde el código Python luego de pasar las pruebas (`needs: pruebas`).
- Genera un ZIP **de implementación** que contiene `application.py`, `app/` y `requirements.txt`, sin `venv`, Git ni archivos de pruebas.
- Publica el paquete mediante `azure/webapps-deploy@v3` usando el perfil de publicación.
- Deja Docker Hub, Render y Railway como trabajos separados, también dependientes de las pruebas.

## Para probar

Sube los archivos al repositorio conservando sus rutas. Haz commit en `main` o ejecuta manualmente el workflow en GitHub Actions mediante **Run workflow**. Inspecciona el trabajo **Desplegar en Azure App Service** y visita el dominio de `dcazure`.

El resultado en GitHub puede indicar un despliegue completado aunque la app falle en iniciar: en ese caso revisa **Registros** y **Diagnosticar y solucionar problemas** en Azure, así como las dos opciones de configuración anteriores.
