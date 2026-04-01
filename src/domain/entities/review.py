from datetime import datetime
import uuid


class Review:
    
    def __init__(self, pr_id: str, review_id: str = None):
        self.pr_id = pr_id
        self.id = review_id if review_id is not None else str(uuid.uuid4())
        self.status = 'pending'
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now()

    def is_approved(self) -> bool:
        if self.rating is None:
            return False
        return self.rating > 70

    def start_processing(self):
        self.status = 'in_progress'

    def complete(self, rating: int, summary: str, recommendations: list):
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.status = 'completed'
        self.completed_at = datetime.now()

    def fail(self, reason: str):
        self.summary = reason
        self.status = 'failed'
        self.completed_at = datetime.now()

    def __repr__(self):
        return f"Review(id={self.id}, pr_id={self.pr_id}, status={self.status})"