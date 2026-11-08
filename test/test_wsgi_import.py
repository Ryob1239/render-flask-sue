"""Evita regresar a los errores `Failed to find attribute app in app`."""
from app import app as wsgi_package_app
from app.app import app as wsgi_module_app


def test_dos_rutas_wsgi_se_refieren_a_la_misma_app():
    assert wsgi_package_app is wsgi_module_app
