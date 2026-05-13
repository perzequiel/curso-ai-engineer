"""Clase 6: GetReviewResultUseCase - Caso de uso para obtener resultado de revision.

Busca y retorna el resultado de una revision existente por pr_id.
"""

from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class ReviewNotFoundError(Exception):
    """Se lanza cuando no se encuentra una revision."""


class GetReviewResultUseCase:
    """Caso de uso: obtener el resultado de una revision de codigo."""

    def __init__(self, review_repository: IReviewRepository):
        self._review_repository = review_repository

    def execute(self, pr_id: str) -> Review:
        """Obtiene el resultado de una revision por pr_id.

        Args:
            pr_id: ID del Pull Request.

        Returns:
            Review con los resultados.

        Raises:
            ReviewNotFoundError: Si no se encuentra la revision.
        """
        review = self._review_repository.find_by_pr_id(pr_id)
        if review is None:
            raise ReviewNotFoundError(f"Review for PR '{pr_id}' not found")
        return review
