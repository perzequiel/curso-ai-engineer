"""Entorno de Alembic.

La URL de conexion se construye desde DatabaseSettings (no desde alembic.ini),
asi una sola fuente de verdad: las variables de entorno / .env.
"""

from __future__ import annotations

from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# Registra los modelos en SQLModel.metadata (necesario para autogenerate).
from src.infrastructure.persistence import models as _models  # noqa: F401
from src.infrastructure.persistence.config import get_database_settings

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Inyecta la URL real (driver sync psycopg) tomada de los settings.
config.set_main_option("sqlalchemy.url", get_database_settings().database_url)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Genera SQL sin conexion (modo --sql)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Aplica migraciones con una conexion real."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
