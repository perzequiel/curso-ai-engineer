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