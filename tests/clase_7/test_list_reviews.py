"""Clase 7: Tests para ListReviewsUseCase.

Verifica el listado de revisiones almacenadas.
"""

from datetime import datetime, timezone, timedelta

import pytest

from src.application.use_cases.list_reviews import ListReviewsUseCase
from src.domain.entities.review import Review
from src.domain.value_objects.rating import Rating
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository


class TestListReviewsUseCase:
    """Tests para el caso de uso de listar revisiones."""

    def setup_method(self):
        self.repository = InMemoryReviewRepository()
        self.use_case = ListReviewsUseCase(review_repository=self.repository)

    def test_execute_returns_empty_list_when_no_reviews(self):
        result = self.use_case.execute()
        assert result == []

    def test_execute_returns_single_review(self):
        review = Review(pr_id="123")
        self.repository.save(review)

        result = self.use_case.execute()
        assert len(result) == 1
        assert result[0].pr_id == "123"

    def test_execute_returns_multiple_reviews(self):
        now = datetime.now(timezone.utc)
        for i in range(3):
            review = Review(
                pr_id=str(i),
                created_at=now + timedelta(seconds=i),
            )
            self.repository.save(review)

        result = self.use_case.execute()
        assert len(result) == 3

    def test_execute_returns_reviews_ordered_by_date(self):
        now = datetime.now(timezone.utc)
        review_old = Review(pr_id="old", created_at=now - timedelta(hours=2))
        review_new = Review(pr_id="new", created_at=now)
        review_mid = Review(pr_id="mid", created_at=now - timedelta(hours=1))

        self.repository.save(review_new)
        self.repository.save(review_old)
        self.repository.save(review_mid)

        result = self.use_case.execute()
        assert result[0].pr_id == "old"
        assert result[1].pr_id == "mid"
        assert result[2].pr_id == "new"

    def test_execute_includes_completed_and_pending_reviews(self):
        pending = Review(pr_id="1")
        completed = Review(pr_id="2")
        completed.complete(
            rating=Rating(90),
            summary="Great",
            recommendations=[],
        )

        self.repository.save(pending)
        self.repository.save(completed)

        result = self.use_case.execute()
        assert len(result) == 2
