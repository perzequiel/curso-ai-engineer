from datetime import datetime, timezone
from domain.value_objects.rating import Rating
from domain.value_objects.review_status import ReviewStatus

class Review:
    def __init__(self, pr_id: str, review_id: str = 'default_id' ):
        self.pr_id = pr_id
        self.id= review_id
        self.status = ReviewStatus.PENDING
        self.rating = Rating()
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)
    
    def is_approved(self):
        return self.rating.is_passing()
    
    def start_processing(self):
        self.status = ReviewStatus.IN_PROGRESS
        return self.status
    
    def complete(self, rating: int , summary: str, recommendations: list[str]): 
        self.rating= Rating(rating)
        self.summary = summary
        self.recommendations= recommendations
        self.status = ReviewStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)

    def fail(self, summary: str): 
        self.summary = summary
        self.status= ReviewStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)  

    def __repr__(self): 
        return f"Valor de Review.ID: {self.id} - Valor de PR_ID: {self.pr_id}"