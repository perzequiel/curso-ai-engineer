"""Engine, session factory e inicializacion de Postgres (sync + pgvector).

Patron tomado de deepflow-monorepo (`backend/app/core/db.py`), adaptado a
sync porque el puerto `IReviewRepository` del curso es sincrono. Si en el
futuro la API pasa a async, se reemplaza por `create_async_engine`.
"""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import Engine, text
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from src.infrastructure.persistence.config import get_database_settings

# Asegura que ReviewModel quede registrado en SQLModel.metadata antes de create_all.
from src.infrastructure.persistence import models as _models  # noqa: F401

# Raiz del repo (donde viven alembic.ini y migrations/).
_REPO_ROOT = Path(__file__).resolve().parents[3]


def create_db_engine(database_url: str | None = None, *, sql_echo: bool | None = None) -> Engine:
    """Crea el engine sync de SQLAlchemy."""
    settings = get_database_settings()
    return create_engine(
        database_url or settings.database_url,
        echo=settings.SQL_ECHO if sql_echo is None else sql_echo,
        future=True,
        pool_pre_ping=True,
    )


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Crea una factory de sesiones ligada al engine."""
    return sessionmaker(
        bind=engine,
        class_=Session,
        expire_on_commit=False,
        autoflush=False,
    )


def init_db(engine: Engine) -> None:
    """Habilita pgvector, crea las tablas y el indice HNSW si no existen.

    Idempotente: seguro de llamar en cada arranque. En produccion real esto
    lo haria Alembic; aca lo hacemos inline para mantener el ejemplo simple.
    """
    dim = get_database_settings().EMBEDDING_DIMENSIONS
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        SQLModel.metadata.create_all(conn)
        conn.execute(
            text(
                "CREATE INDEX IF NOT EXISTS reviews_embedding_hnsw "
                "ON reviews USING hnsw (embedding vector_cosine_ops)"
            )
        )
    _ = dim  # documentado: la dimension del indice la fija la columna Vector(dim)


def run_migrations() -> None:
    """Aplica las migraciones de Alembic hasta head.

    Es la forma canonica de crear/actualizar el esquema en produccion.
    Idempotente: si la DB ya esta en head, no hace nada. Se llama al
    arrancar la app con backend de Postgres (ver http_api._build_repository).
    """
    from alembic import command  # noqa: PLC0415
    from alembic.config import Config  # noqa: PLC0415

    cfg = Config(str(_REPO_ROOT / "alembic.ini"))
    cfg.set_main_option("script_location", str(_REPO_ROOT / "migrations"))
    command.upgrade(cfg, "head")


def close_db(engine: Engine) -> None:
    """Cierra el pool de conexiones. Llamar en shutdown de la app."""
    engine.dispose()
