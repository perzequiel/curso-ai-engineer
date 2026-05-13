"""Clase 1: Review - Entidad principal del dominio.

Representa una revision de codigo realizada sobre un Pull Request.
"""

from datetime import datetime, timezone
from uuid import uuid4

from src.domain.value_objects.rating import Rating
from src.domain.value_objects.review_status import ReviewStatus


class Review:
    """Entidad que representa una revision de codigo."""

    def __init__(
        self,
        pr_id: str,
        review_id: str | None = None,
        status: ReviewStatus = ReviewStatus.PENDING,
        rating: Rating | None = None,
        summary: str = "",
        recommendations: list[str] | None = None,
        created_at: datetime | None = None,
        completed_at: datetime | None = None,
    ):
        self.id = review_id or str(uuid4())
        self.pr_id = pr_id
        self.status = status
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations or []
        self.created_at = created_at or datetime.now(timezone.utc)
        self.completed_at = completed_at

    def is_approved(self) -> bool:
        """Determina si la revision fue aprobada (rating > 70)."""
        if self.rating is None:
            return False
        return self.rating.is_passing()

    def complete(self, rating: Rating, summary: str, recommendations: list[str]) -> None:
        """Marca la revision como completada con resultados."""
        self.status = ReviewStatus.COMPLETED
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, reason: str) -> None:
        """Marca la revision como fallida."""
        self.status = ReviewStatus.FAILED
        self.summary = f"Review failed: {reason}"
        self.completed_at = datetime.now(timezone.utc)

    def start_processing(self) -> None:
        """Marca la revision como en progreso."""
        self.status = ReviewStatus.IN_PROGRESS

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id!r}, pr_id={self.pr_id!r}, "
            f"status={self.status.value}, rating={self.rating})"
        )
