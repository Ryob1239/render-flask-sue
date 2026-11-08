"""Punto de entrada WSGI compartido por Render y Railway.

Permite tanto `gunicorn app:app` como `gunicorn app.app:app`,
conservando los imports de las pruebas y de Azure.
"""
from .app import app

__all__ = ["app"]
