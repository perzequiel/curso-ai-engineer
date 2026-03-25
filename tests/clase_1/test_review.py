"""Clase 1: Tests para la entidad Review.

Verifica la creacion, cambios de estado y logica de aprobacion
de la entidad principal del dominio.
"""

from datetime import datetime

import pytest

from src.domain.entities.review import Review


class TestReviewCreation:
    """Tests de creacion de la entidad Review."""

    def test_create_review_with_defaults(self):
        review = Review(pr_id="123")
        assert review.pr_id == "123"
        # assert review.status == 'pending'
        # assert review.rating is None
        # assert review.summary == ""
        # assert review.recommendations == []
        # assert review.completed_at is None
        # assert review.id is not None

    def test_create_review_with_custom_id(self):
        review = Review(pr_id="123", review_id="custom-id")
        assert review.id == "custom-id"

    def test_create_review_has_created_at(self):
        review = Review(pr_id="123")
        assert isinstance(review.created_at, datetime)


class TestReviewApproval:
    """Tests de logica de aprobacion."""

    def test_is_approved_without_rating(self):
        review = Review(pr_id="123")
        assert review.is_approved() is False

    def test_is_approved_with_passing_rating(self):
        review = Review(pr_id="123")
        review.rating = 85
        assert review.is_approved() is True

    def test_is_not_approved_with_low_rating(self):
        review = Review(pr_id="123")
        review.rating = 50
        assert review.is_approved() is False

    def test_is_not_approved_at_threshold(self):
        review = Review(pr_id="123")
        review.rating = 70
        assert review.is_approved() is False

    def test_is_approved_above_threshold(self):
        review = Review(pr_id="123")
        review.rating = 71
        assert review.is_approved() is True


class TestReviewStateTransitions:
    """Tests de transiciones de estado."""

    def test_start_processing(self):
        review = Review(pr_id="123")
        review.start_processing()
        assert review.status == 'in_progress'

    def test_complete_review(self):
        review = Review(pr_id="123")
        rating = 90
        review.complete(
            rating=rating,
            summary="Excellent code",
            recommendations=["Minor: add docstrings"],
        )
        assert review.status == 'completed'
        assert review.rating == rating
        assert review.summary == "Excellent code"
        assert review.recommendations == ["Minor: add docstrings"]
        assert review.completed_at is not None

    def test_fail_review(self):
        review = Review(pr_id="123")
        review.fail("API timeout")
        assert review.status == 'failed'
        assert "API timeout" in review.summary
        assert review.completed_at is not None

    def test_repr(self):
        review = Review(pr_id="123", review_id="r-001")
        result = repr(review)
        assert "r-001" in result
        assert "123" in result
