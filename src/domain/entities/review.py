import uuid
from datetime import datetime, timezone

from src.domain.value_objects.review_status import ReviewStatus
from src.domain.value_objects.rating import Rating

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None, rating: Rating | None = None, created_at: datetime | None = None):
        self.id = review_id or str(uuid.uuid4())
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = created_at or datetime.now(timezone.utc)


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
            f"status={self.status}, rating={self.rating})"
        )