from datetime import datetime, timezone
from src.domain.value_objects.review_status import ReviewStatus
from src.domain.value_objects.rating import Rating
APPROVAL_THRESHOLD = 70;

class Review:
    def __init__(self, pr_id: str, review_id: str | None = None, rating : Rating | None = None):
        self.id = review_id or ""
        self.pr_id = pr_id
        self.status = ReviewStatus.PENDING
        self.rating = rating
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.created_at = datetime.now(timezone.utc)
        
    def is_approved(self) -> bool:
        """Validate rating"""
        if self.rating is None:
            return False
        return self.rating.is_passing()
    
    def start_processing(self) -> None:
        """Start the PR"""
        self.status = ReviewStatus.IN_PROGRESS
    
    def complete(self,rating: Rating, summary: str, recommendations: str ) -> None:
        """Complete the PR"""
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.status = ReviewStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        
    def fail(self, summary: str) -> None:
        """Fail PR"""
        self.summary = summary
        self.status = ReviewStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)
        
    def __repr__(self) -> str:
        return (
            f"Review(id={self.id!r}, pr_id={self.pr_id!r},"
            f"status={self.status}, rating={self.rating }"   
        )
        
