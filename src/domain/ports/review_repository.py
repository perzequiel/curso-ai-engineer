from abc import ABC, abstractmethod
from typing import Optional, List
from src.domain.entities.review import Review


class IReviewRepository(ABC):
    """Interface abstracta para el repositorio de Reviews.
    
    Define el contrato que deben cumplir todas las implementaciones
    de repositorios de reviews, siguiendo el principio de inversión
    de dependencias (DIP) de SOLID.
    """

    @abstractmethod
    def save(self, review: Review) -> Review:
        """Guarda una review en el repositorio."""
        pass

    @abstractmethod
    def find_by_pr_id(self, pr_id: str) -> Optional[Review]:
        """Busca una review por su PR ID."""
        pass

    @abstractmethod
    def find_by_id(self, review_id: str) -> Optional[Review]:
        """Busca una review por su ID."""
        pass

    @abstractmethod
    def find_all(self) -> List[Review]:
        """Retorna todas las reviews."""
        pass

    @abstractmethod
    def delete(self, review_id: str) -> bool:
        """Elimina una review por su ID. Retorna True si se eliminó."""
        pass
