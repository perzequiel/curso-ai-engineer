from datetime import datetime, timezone 

from src.domain.value_objects.review_status import ReviewStatus
from src.domain.value_objects.rating import Rating

APPROVAL_THRESHOLD = 70

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None, rating: Rating | None = None):
        self.id = review_id or "some_id"
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)

    def is_approved(self) -> bool:
        """Determines if the review is approved based on its (rating > 70)."""
        if self.rating is None:
            return False
        return self.rating.value > APPROVAL_THRESHOLD
    
    """ rating, summary, recommendations will be provided by the LLM so when completing the review. """
    def complete(self, rating: Rating, summary: str, recommendations: list[str]):
        """Completes the review with the given rating, summary and recommendations."""
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.status = ReviewStatus.COMPLETED                                          
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, reason: str) -> None:
        """Fails the review with the given summary and recommendations."""
        self.summary = f"Review failed: {reason}"
        self.status = ReviewStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)

    def start_processing(self) -> None:
        """Starts processing the review."""
        self.status = ReviewStatus.IN_PROGRESS

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id!r}, pr_id={self.pr_id!r}, "
            f"status={self.status}, rating={self.rating})"
        )