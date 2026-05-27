"""Configuracion de la base de datos Postgres (pgvector).

Aislada en el adaptador de persistencia: el dominio y los casos de uso
no conocen estos detalles. Si no hay Postgres configurado, la API cae
automaticamente al repositorio en memoria (ver http_api._build_repository).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Settings de Postgres leidos desde variables de entorno / .env."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Si DATABASE_URL viene seteada, tiene prioridad sobre las partes sueltas.
    DATABASE_URL: str | None = None

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "app"
    POSTGRES_PASSWORD: str = "changethis"  # noqa: S105
    POSTGRES_DB: str = "curso_ai"

    # Debe coincidir con Vector(n) del modelo. 1536 = OpenAI text-embedding-3-small.
    EMBEDDING_DIMENSIONS: int = 1536

    # Echo de SQL para debug.
    SQL_ECHO: bool = False

    @property
    def database_url(self) -> str:
        """URL sync con driver psycopg3 (postgresql+psycopg://)."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache
def get_database_settings() -> DatabaseSettings:
    """Devuelve los settings cacheados (un solo parseo por proceso)."""
    return DatabaseSettings()
