"""Clase 7: ListReviewsUseCase - Caso de uso para listar revisiones.

Retorna todas las revisiones almacenadas en el repositorio.
"""

from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class ListReviewsUseCase:
    """Caso de uso: listar todas las revisiones de codigo."""

    def __init__(self, review_repository: IReviewRepository):
        self._review_repository = review_repository

    def execute(self) -> list[Review]:
        """Obtiene todas las revisiones ordenadas por fecha.

        Returns:
            Lista de revisiones ordenadas por fecha de creacion.
        """
        return self._review_repository.find_all()
