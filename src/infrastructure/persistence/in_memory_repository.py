"""Clase 8: InMemoryReviewRepository - Adaptador de persistencia en memoria.

Implementacion concreta del puerto IReviewRepository que almacena
las revisiones en memoria. Ideal para testing y desarrollo.
"""

from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class InMemoryReviewRepository(IReviewRepository):
    """Repositorio de revisiones en memoria."""

    def __init__(self) -> None:
        self._reviews: dict[str, Review] = {}

    def save(self, review: Review) -> Review:
        """Guarda o actualiza una revision en memoria."""
        self._reviews[review.id] = review
        return review

    def find_by_pr_id(self, pr_id: str) -> Review | None:
        """Busca una revision por el ID del Pull Request."""
        for review in self._reviews.values():
            if review.pr_id == pr_id:
                return review
        return None

    def find_by_id(self, review_id: str) -> Review | None:
        """Busca una revision por su ID unico."""
        return self._reviews.get(review_id)

    def find_all(self) -> list[Review]:
        """Retorna todas las revisiones ordenadas por fecha de creacion."""
        return sorted(
            self._reviews.values(),
            key=lambda r: r.created_at,
        )

    def delete(self, review_id: str) -> bool:
        """Elimina una revision por su ID."""
        if review_id in self._reviews:
            del self._reviews[review_id]
            return True
        return False

    def clear(self) -> None:
        """Limpia todas las revisiones. Util para testing."""
        self._reviews.clear()
