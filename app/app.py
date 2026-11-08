import os
from flask import Flask, render_template

app = Flask(__name__, static_folder='static', template_folder='templates')

def detectar_entorno():
    # Detectar Render
    if os.environ.get('RENDER'):
        return {"nombre": "Render", "imagen": "render.png"}
    
    # Detectar Railway
    elif os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_STATIC_URL'):
        return {"nombre": "Railway", "imagen": "railway.png"}
    
    # Detectar Azure App Service
    elif os.environ.get('WEBSITE_SITE_NAME'):
        return {"nombre": "Azure App Service", "imagen": "azure.png"}
    
    # Detectar contenedor Docker (inyectado por nuestro Dockerfile)
    elif os.environ.get('DOCKER_ENV'):
        return {"nombre": "Docker Hub / Contenedor", "imagen": "docker.png"}
    
    # Si no hay variables, asume que es ejecución local
    else:
        return {"nombre": "Entorno Local", "imagen": "local.png"}

@app.route('/')
def index():
    entorno_actual = detectar_entorno()
    return render_template(
        'index.html', 
        entorno=entorno_actual["nombre"], 
        imagen=entorno_actual["imagen"]
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)