"""Modelos ORM (SQLModel) para la capa de persistencia Postgres.

Estos modelos viven SOLO en el adaptador: el dominio (`src/domain/entities`)
no depende de SQLModel ni de la base de datos. Aca traducimos entre la
entidad de dominio `Review` y la fila `ReviewModel`.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, DateTime
from sqlalchemy.types import JSON
from sqlmodel import Field, SQLModel

from src.domain.entities.review import Review
from src.domain.value_objects.rating import Rating
from src.domain.value_objects.review_status import ReviewStatus
from src.infrastructure.persistence.config import get_database_settings

_EMBEDDING_DIM = get_database_settings().EMBEDDING_DIMENSIONS


class ReviewModel(SQLModel, table=True):
    """Tabla `reviews`. Espejo persistente de la entidad de dominio Review.

    La columna `embedding` (pgvector) es opcional: habilita busqueda
    semantica sobre el summary sin acoplar el dominio a la DB.
    """

    __tablename__ = "reviews"

    id: str = Field(primary_key=True)
    pr_id: str = Field(index=True)
    status: str = Field(default=ReviewStatus.PENDING.value)
    rating: int | None = Field(default=None)
    summary: str = Field(default="")
    recommendations: list[str] = Field(
        default_factory=list, sa_column=Column(JSON, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )
    completed_at: datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )
    embedding: Any = Field(
        default=None, sa_column=Column(Vector(_EMBEDDING_DIM), nullable=True)
    )

    # -- Mapeo dominio <-> persistencia ------------------------------------

    @classmethod
    def from_domain(cls, review: Review) -> "ReviewModel":
        """Construye una fila nueva a partir de la entidad de dominio."""
        return cls(
            id=review.id,
            pr_id=review.pr_id,
            status=review.status.value,
            rating=review.rating.value if review.rating else None,
            summary=review.summary,
            recommendations=list(review.recommendations),
            created_at=review.created_at,
            completed_at=review.completed_at,
        )

    def apply_domain(self, review: Review) -> None:
        """Actualiza los campos de dominio sobre una fila existente.

        No toca `embedding`: el dominio no lo conoce, lo gestiona el indexador.
        """
        self.pr_id = review.pr_id
        self.status = review.status.value
        self.rating = review.rating.value if review.rating else None
        self.summary = review.summary
        self.recommendations = list(review.recommendations)
        self.created_at = review.created_at
        self.completed_at = review.completed_at

    def to_domain(self) -> Review:
        """Reconstruye la entidad de dominio desde la fila."""
        return Review(
            review_id=self.id,
            pr_id=self.pr_id,
            status=ReviewStatus(self.status),
            rating=Rating(self.rating) if self.rating is not None else None,
            summary=self.summary,
            recommendations=list(self.recommendations or []),
            created_at=self.created_at,
            completed_at=self.completed_at,
        )
