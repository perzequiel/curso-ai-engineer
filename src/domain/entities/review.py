import datetime
import typing
import uuid
import enum

class ReviewStatus(enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class Review:
    def __init__(self, pr_id: str, review_id: str = None):
        self.pr_id = pr_id
        self.id = review_id or str(uuid.uuid4())
        self.created_at = datetime.datetime.now()
        self.status = 'pending'
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None

    def is_approved(self) -> bool:
        return self.rating is not None and self.rating > 70

    def start_processing(self):
        self.status = 'in_progress'

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.status = 'completed'
        self.completed_at = datetime.datetime.now()
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations

    def fail(self, comment: str):
        self.status = 'failed'
        self.summary = comment
        self.completed_at = datetime.datetime.now()

    def repr(self, review):
        self.summary = review.summary
        self.reason = review.reason
    
    def __repr__(self):
        return f"Review(id={self.id}, pr_id={self.pr_id}, status={self.status}, rating={self.rating}, comment={self.summary})"
