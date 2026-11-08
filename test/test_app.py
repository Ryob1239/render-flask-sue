import pytest
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_status(client):
    """Verifica que el endpoint principal responda con un 200 OK."""
    response = client.get('/')
    assert response.status_code == 200

def test_index_content_local(client):
    """Verifica que el HTML renderice correctamente el contenido base y la imagen local."""
    response = client.get('/')
    html = response.get_data(as_text=True)
    
    assert "¡Despliegue Completado!" in html
    assert "Entorno Local" in html
    assert "local.png" in html

def test_error_intencional():
    assert 1 == 2, "ERROR: Prueba fallida intencionalmente"