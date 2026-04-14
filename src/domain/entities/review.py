from datetime import datetime, timezone
import uuid
from src.domain.value_objects.reviewStatus import ReviewStatus
from src.domain.value_objects.rating import Rating

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None, rating: strg | None = None):
        self.id = review_id or str(uuid.uuid4())
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)

        if review_id is not None:
            self.id = review_id

    def is_approved(self) -> bool:
        """Determina si la revision fue aprobada (rating > 70)."""
        return self.rating is not None and Rating.in_range(self.rating)
    
    def start_processing(self) -> None:
        """Marca la revision como en progreso."""
        self.status = ReviewStatus.IN_PROGRESS

    def complete(self, rating: int, summary: str, recommendations: list[str]) -> None:
        self.status = ReviewStatus.COMPLETED
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now()

    def fail(self, message: str) -> None:
        """Marca la revision como fallida."""
        self.status = ReviewStatus.FAILED
        self.summary = message
        self.completed_at = datetime.now()

    def __repr__(self) -> str:
        return f"Review(id={self.id}, pr_id={self.pr_id})"


