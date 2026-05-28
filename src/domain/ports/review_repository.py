from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.review import Review

class IReviewRepository(ABC):
    """Interface para el repositorio de reviews."""

    @abstractmethod
    def save(self, review: Review) -> Review:
        """Toma el objeto de dominio, la review y lo guarda en el repositorio."""
        pass

    @abstractmethod
    def find_by_pr_id(self, pr_id: str) -> Review | None:
        """Encuentra reviews por ID de PR."""
        pass

    @abstractmethod
    def find_by_id(self, review_id: str) -> Review | None:
        """Encuentra una review por su ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Review]:
        """Encuentra todas las reviews."""
        pass

    @abstractmethod
    def delete(self, review_id: str) -> bool:
        """Elimina una review por su ID."""
        pass