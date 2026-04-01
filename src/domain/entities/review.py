from datetime import datetime, timezone


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
