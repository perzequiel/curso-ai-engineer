from datetime import datetime, timezone
from src.domain.value_objects.review_status import ReviewStatus
from src.domain.value_objects.rating import Rating

class Review:
    def __init__(self, pr_id: str, review_id: int = '123', rating: Rating | None = None):
        self.pr_id = pr_id
        self.id = review_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)


    def is_approved(self) -> bool:
        """Determinamos si es aprobado (rating > 70)"""

        if self.rating is None:
            return False
        return self.rating.is_approved()   


    def start_processing(self) -> str:
        self.status = ReviewStatus.IN_PROGRESS  


    def complete(self, rating: Rating, summary: str, recommendations: []) -> None:
        self.status = ReviewStatus.COMPLETED
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now(timezone.utc)


    def fail(self, failMsg: str) -> None:
        self.status = ReviewStatus.FAILED
        self.summary = f"Review failed: {failMsg}"
        self.completed_at = datetime.now(timezone.utc)


    def __repr__(self) -> str:
        return (
            f"Review(id={self.id!r}), pr_id={self.pr_id!r}, "
            f"status(id={self.status}), rating={self.rating}"
        )