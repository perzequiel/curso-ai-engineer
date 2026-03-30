from datetime import datetime
from src.domain.entities.enums import ReviewStatus

class Review:
    def __init__(self, pr_id: str, review_id: int = '123'):
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = review_id
        self.created_at = datetime.now()
    
    def is_approved(self) -> bool:
        return self.rating is not None and self.rating > 80

    def start_processing(self):
        self.status = ReviewStatus.IN_PROGRESS
    
    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.status = ReviewStatus.COMPLETED
        self.completed_at = datetime.now()
    
    def fail(self, summary: str):
        self.status = ReviewStatus.FAILED
        self.summary = summary
        self.completed_at = datetime.now()

    def __repr__(self):
        return f"Review(id={self.id}, pr_id={self.pr_id})"
