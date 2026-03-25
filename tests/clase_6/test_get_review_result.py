"""Clase 6: Tests para GetReviewResultUseCase.

Verifica la busqueda y retorno de resultados de revisiones.
"""

import pytest

from src.application.use_cases.get_review_result import (
    GetReviewResultUseCase,
    ReviewNotFoundError,
)
from src.domain.entities.review import Review
from src.domain.value_objects.rating import Rating
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository


class TestGetReviewResultUseCase:
    """Tests para el caso de uso de obtener resultado de revision."""

    def setup_method(self):
        self.repository = InMemoryReviewRepository()
        self.use_case = GetReviewResultUseCase(review_repository=self.repository)

    def test_execute_returns_existing_review(self):
        review = Review(pr_id="123", review_id="r-001")
        review.complete(
            rating=Rating(85),
            summary="Good code",
            recommendations=["Add tests"],
        )
        self.repository.save(review)

        result = self.use_case.execute(pr_id="123")
        assert result.id == "r-001"
        assert result.pr_id == "123"
        assert result.rating == Rating(85)

    def test_execute_raises_error_for_nonexistent_review(self):
        with pytest.raises(ReviewNotFoundError) as exc_info:
            self.use_case.execute(pr_id="nonexistent")
        assert "nonexistent" in str(exc_info.value)

    def test_execute_returns_pending_review(self):
        review = Review(pr_id="456")
        self.repository.save(review)

        result = self.use_case.execute(pr_id="456")
        assert result.pr_id == "456"
        assert result.rating is None

    def test_execute_returns_failed_review(self):
        review = Review(pr_id="789")
        review.fail("Timeout")
        self.repository.save(review)

        result = self.use_case.execute(pr_id="789")
        assert "Timeout" in result.summary
