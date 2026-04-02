from datetime import datetime, timezone

APPROVAL_THRESHOLD = 70

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None):
        self.id = review_id or "some_id"
        self.pr_id = pr_id
        self.status = 'pending'
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)

    def is_approved(self):
        if self.rating is None:
            return False
        return self.rating > APPROVAL_THRESHOLD
    
    def start_processing(self):
        self.status = 'in_progress'

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.status = 'completed'
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, summary: str) -> None:
        self.summary = summary
        self.status = 'failed'
        self.completed_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        outcome: str = ""
        outcome = f"Review - ID: {self.id!r} - PR ID: {self.pr_id!r}"
        return outcome
