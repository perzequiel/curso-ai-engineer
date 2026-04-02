from datetime import datetime, timezone

class Review:
    def __init__(self, pr_id: str, review_id: int = '123'):
        self.pr_id = pr_id
        self.id = review_id
        self.status = 'pending'
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)
