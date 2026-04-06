from datetime import datetime, timezone

from src.domain.value_objects.review_status import ReviewStatus
from domain.value_objects.rating import Rating

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None, rating: Rating | None = None):
        self.pr_id = pr_id
        self.id = review_id or 'some_id'
        self.created_at = datetime.now(timezone.utc)
        self.rating = Rating(rating)
        self.status = ReviewStatus.PENDING
        self.summary = ""
        self.recommendations = []
        self.completed_at = None

    def is_approved(self) -> bool:
        if self.rating.value is None:
            return False
        return self.rating.is_passing()
    
    def start_processing(self):
        self.status = ReviewStatus.IN_PROGRESS

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.rating = Rating(rating)
        self.status = ReviewStatus.COMPLETED
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now()

    def fail(self, summary: str):
        self.status = ReviewStatus.FAILED
        self.summary = summary
        self.completed_at = datetime.now()

    def __repr__(self):
        return f"<Review id={self.id} pr_id={self.pr_id} status={self.status}>"