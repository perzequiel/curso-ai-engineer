from datetime import datetime, timezone
import time

APPROVAL_THRESHOLD = 70


class Review:
    def __init__(self, pr_id: str, review_id: str | None = None):
        self.pr_id = pr_id
        self.status = "pending"
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = review_id or "some_id"
        self.created_at = datetime.now(timezone.utc)

    def is_approved(self) -> bool:
        if self.rating is None:
            return False

        return self.rating > APPROVAL_THRESHOLD

    def start_processing(self) -> str:
        self.status = "in_progress"
        pass

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.status = "completed"
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, reason: str):
        self.status = "failed"
        self.summary = reason
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return (
            f"Review(id={self.id}, pr_id={self.pr_id},"
            f"status={self.status}, rating={self.rating})"
        )
