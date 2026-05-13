"""Entrypoint para FastAPI CLI.

Ejecutar con:
    fastapi dev          # modo desarrollo (con auto-reload)
    fastapi run          # modo produccion

La logica HTTP vive en `src/infrastructure/api/http_api.py` como un
adaptador mas dentro de la arquitectura hexagonal. Este archivo solo
re-exporta la instancia `app` para que el CLI de FastAPI la detecte.
"""

from src.infrastructure.api.http_api import app

__all__ = ["app"]
