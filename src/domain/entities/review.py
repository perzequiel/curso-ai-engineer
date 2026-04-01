from datetime import datetime, timezone

from src.domain.value_objects.rating import Rating
from src.domain.value_objects.review_status import ReviewStatus


APPROVAL_THRESHOLD = 70


class Review:
    def __init__(
        self, pr_id: str, review_id: str | None = None, rating: Rating | None = None
    ):
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = review_id or "some_id"
        self.created_at = datetime.now(timezone.utc)

    def is_approved(self) -> bool:
        if self.rating is None:
            return False

        return self.rating.is_passing()

    def start_processing(self) -> None:
        self.status = ReviewStatus.IN_PROGRESS
        pass

    def complete(
        self, rating: Rating, summary: str, recommendations: list[str]
    ) -> None:
        self.status = ReviewStatus.COMPLETED
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, reason: str) -> None:
        self.status = ReviewStatus.FAILED
        self.summary = reason
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id}, pr_id={self.pr_id},"
            f"status={self.status}, rating={self.rating})"
        )
