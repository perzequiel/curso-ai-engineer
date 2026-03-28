from datetime import datetime, timezone
from domain.enums.review_status import ReviewStatus
from src.domain.value_objects.rating import Rating
class Review:
    def __init__(self, pr_id: str, review_id: str = 'default_id'):
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = review_id
        self.created_at = datetime.now(timezone.utc)

    def is_approved(self) -> bool: 
        if self.rating is None:
            return False
        return self.rating.is_passing()
    
    def start_processing(self) -> None:
        self.status = ReviewStatus.IN_PROGRESS

    def complete(self, rating: Rating, summary: str, recommendations: list[str]) -> None:
        self.status = ReviewStatus.COMPLETED
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, summary: str) -> None:
        self.summary = summary
        self.status = ReviewStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Review(pr_id='{self.pr_id}', review_id='{self.id}')"
