import datetime
import typing
import uuid
import enum
from typing import Optional
from src.domain.entities.rating import Rating

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
        self.status = ReviewStatus.PENDING
        self._rating: Optional[Rating] = None  # Privado
        self.summary = ""
        self.recommendations = []
        self.completed_at = None

    @property
    def rating(self) -> Optional[int]:
        """Obtiene el valor numérico del rating."""
        return self._rating.value if self._rating else None
    
    @rating.setter
    def rating(self, value: Optional[int]):
        """Establece el rating creando un objeto Rating."""
        self._rating = Rating(value) if value is not None else None
    
    def is_approved(self) -> bool:
        """Delega la lógica de aprobación a la clase Rating."""
        return self._rating is not None and self._rating.is_approved()

    def start_processing(self):
        self.status = ReviewStatus.IN_PROGRESS

    def complete(self, rating: int, summary: str, recommendations: list[str]):
        self.status = ReviewStatus.COMPLETED
        self.rating = rating  # Usa el setter
        self.summary = summary
        self.recommendations = recommendations
        self.completed_at = datetime.datetime.now()

    def fail(self, comment: str):
        self.status = ReviewStatus.FAILED
        self.summary = comment
        self.completed_at = datetime.datetime.now()
    
    def __repr__(self):
        return f"Review(id={self.id}, pr_id={self.pr_id})"
