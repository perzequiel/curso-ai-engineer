"""Clase 8: Tests para InMemoryReviewRepository.

Verifica la implementacion concreta del repositorio en memoria,
validando todas las operaciones CRUD.
"""

import pytest

from src.domain.entities.review import Review
from src.domain.value_objects.rating import Rating
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository


class TestInMemoryReviewRepository:
    """Tests para el repositorio en memoria."""

    def setup_method(self):
        self.repository = InMemoryReviewRepository()

    def test_save_and_find_by_id(self):
        review = Review(pr_id="123", review_id="r-001")
        self.repository.save(review)

        found = self.repository.find_by_id("r-001")
        assert found is not None
        assert found.id == "r-001"
        assert found.pr_id == "123"

    def test_save_returns_review(self):
        review = Review(pr_id="123")
        result = self.repository.save(review)
        assert result.id == review.id

    def test_find_by_pr_id(self):
        review = Review(pr_id="456", review_id="r-002")
        self.repository.save(review)

        found = self.repository.find_by_pr_id("456")
        assert found is not None
        assert found.pr_id == "456"

    def test_find_by_pr_id_returns_none_when_not_found(self):
        result = self.repository.find_by_pr_id("nonexistent")
        assert result is None

    def test_find_by_id_returns_none_when_not_found(self):
        result = self.repository.find_by_id("nonexistent")
        assert result is None

    def test_find_all_empty(self):
        result = self.repository.find_all()
        assert result == []

    def test_find_all_returns_all_reviews(self):
        for i in range(3):
            self.repository.save(Review(pr_id=str(i)))

        result = self.repository.find_all()
        assert len(result) == 3

    def test_find_all_ordered_by_created_at(self):
        from datetime import datetime, timezone, timedelta

        now = datetime.now(timezone.utc)
        r1 = Review(pr_id="1", created_at=now - timedelta(hours=2))
        r2 = Review(pr_id="2", created_at=now)
        r3 = Review(pr_id="3", created_at=now - timedelta(hours=1))

        self.repository.save(r2)
        self.repository.save(r1)
        self.repository.save(r3)

        result = self.repository.find_all()
        assert result[0].pr_id == "1"
        assert result[1].pr_id == "3"
        assert result[2].pr_id == "2"

    def test_delete_existing_review(self):
        review = Review(pr_id="123", review_id="r-del")
        self.repository.save(review)

        result = self.repository.delete("r-del")
        assert result is True
        assert self.repository.find_by_id("r-del") is None

    def test_delete_nonexistent_review(self):
        result = self.repository.delete("nonexistent")
        assert result is False

    def test_update_existing_review(self):
        review = Review(pr_id="123", review_id="r-upd")
        self.repository.save(review)

        review.complete(
            rating=Rating(75),
            summary="Updated",
            recommendations=["Fix imports"],
        )
        self.repository.save(review)

        found = self.repository.find_by_id("r-upd")
        assert found.summary == "Updated"
        assert found.rating == Rating(75)

    def test_clear(self):
        for i in range(5):
            self.repository.save(Review(pr_id=str(i)))

        self.repository.clear()
        assert self.repository.find_all() == []
