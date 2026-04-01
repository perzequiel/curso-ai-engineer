from datetime import datetime

class Review:
    def __init__(self, pr_id: str, review_id: str = None):
        self.pr_id = pr_id
        self.status = 'pending'
        self.rating = None
        self.summary = ""
        self.recommendations = []
        self.completed_at = None
        self.id = pr_id
        self.created_at = datetime.now()

        if review_id is not None:
            self.id = review_id

    def is_approved(self):
        if self.rating is None or self.rating <= 70:
            return False
        return True
    
    def start_processing(self):
        self.status = 'in_progress'

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.status = 'completed'
        self.rating = rating
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.now()

    def fail(self, message: str):
        self.status = 'failed'
        self.summary = message
        self.completed_at = datetime.now()

    def __repr__(self):
        return f"Review(id={self.id}, pr_id={self.pr_id})"


