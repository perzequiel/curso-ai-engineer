"""Fixtures compartidas para los tests del curso."""

import pytest

from src.domain.entities.review import Review


@pytest.fixture
def sample_review() -> Review:
    """Crea una revision de ejemplo."""
    return Review(pr_id="123", review_id="review-001")


@pytest.fixture
def completed_review() -> Review:
    """Crea una revision completada de ejemplo."""
    review = Review(pr_id="456", review_id="review-002")
    review.complete(
        rating=Rating(85),
        summary="Good code quality overall",
        recommendations=["Add more tests", "Improve error handling"],
    )
    return review


@pytest.fixture
def failed_review() -> Review:
    """Crea una revision fallida de ejemplo."""
    review = Review(pr_id="789", review_id="review-003")
    review.fail("GitHub API timeout")
    return review


