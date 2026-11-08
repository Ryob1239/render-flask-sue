"""Punto de entrada de Azure App Service (Linux / Python).

La aplicación real se mantiene en app/app.py. Azure detecta este archivo
y puede arrancar Gunicorn con application:app.
"""
from app.app import app
