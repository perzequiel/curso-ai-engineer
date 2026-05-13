"""Clase 2: IReviewRepository - Puerto para persistencia de revisiones.

Define la interface abstracta que cualquier implementacion de
repositorio debe cumplir para almacenar y recuperar revisiones.
"""

from abc import ABC, abstractmethod

from src.domain.entities.review import Review


class IReviewRepository(ABC):
    """Interface abstracta para el repositorio de revisiones."""

    @abstractmethod
    def save(self, review: Review) -> Review:
        """Guarda o actualiza una revision en el repositorio."""
        ...

    @abstractmethod
    def find_by_pr_id(self, pr_id: str) -> Review | None:
        """Busca una revision por el ID del Pull Request."""
        ...

    @abstractmethod
    def find_by_id(self, review_id: str) -> Review | None:
        """Busca una revision por su ID unico."""
        ...

    @abstractmethod
    def find_all(self) -> list[Review]:
        """Retorna todas las revisiones ordenadas por fecha de creacion."""
        ...

    @abstractmethod
    def delete(self, review_id: str) -> bool:
        """Elimina una revision por su ID. Retorna True si fue eliminada."""
        ...
