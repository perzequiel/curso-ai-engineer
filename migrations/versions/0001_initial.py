"""initial: extension pgvector + tabla reviews + indice HNSW

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-27
"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

from src.infrastructure.persistence.config import get_database_settings

revision: str = "0001_initial"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

_EMBEDDING_DIM = get_database_settings().EMBEDDING_DIMENSIONS


def upgrade() -> None:
    # pgvector debe existir antes de crear la columna Vector.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "reviews",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("pr_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=True),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("embedding", Vector(_EMBEDDING_DIM), nullable=True),
    )
    op.create_index("ix_reviews_pr_id", "reviews", ["pr_id"])
    # Indice HNSW para busqueda por similitud coseno (operador <=> de pgvector).
    op.execute(
        "CREATE INDEX IF NOT EXISTS reviews_embedding_hnsw "
        "ON reviews USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS reviews_embedding_hnsw")
    op.drop_index("ix_reviews_pr_id", table_name="reviews")
    op.drop_table("reviews")
    op.execute("DROP EXTENSION IF EXISTS vector")
