from datetime import datetime, timezone
from src.domain.constants import APPROVAL_THRESHOLD


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


    def is_approved(self) -> bool:
        """Determinamos si es aprobado (rating > 70)"""

        if self.rating is None:
            return False
        return self.rating > APPROVAL_THRESHOLD    


    def start_processing(self) -> str:
        self.status = 'in_progress'   