"""Fixtures compartidas para los tests del curso."""

import pytest

# Comentado temporalmente para permitir que los tests de clase 2 ejecuten
# Se descomentará cuando se implementen los módulos correspondientes
# from src.domain.entities.review import Review
# from src.domain.value_objects.rating import Rating
# from src.domain.value_objects.review_status import ReviewStatus
# from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository
# from src.infrastructure.ai.ai_code_reviewer import MockCodeReviewer
# from src.infrastructure.github.github_adapter import MockGitHubAdapter


# @pytest.fixture
# def sample_review() -> Review:
#     """Crea una revision de ejemplo."""
#     return Review(pr_id="123", review_id="review-001")


# @pytest.fixture
# def completed_review() -> Review:
#     """Crea una revision completada de ejemplo."""
#     review = Review(pr_id="456", review_id="review-002")
#     review.complete(
#         rating=Rating(85),
#         summary="Good code quality overall",
#         recommendations=["Add more tests", "Improve error handling"],
#     )
#     return review


# @pytest.fixture
# def failed_review() -> Review:
#     """Crea una revision fallida de ejemplo."""
#     review = Review(pr_id="789", review_id="review-003")
#     review.fail("GitHub API timeout")
#     return review


# @pytest.fixture
# def in_memory_repository() -> InMemoryReviewRepository:
#     """Crea un repositorio en memoria limpio."""
#     return InMemoryReviewRepository()


# @pytest.fixture
# def mock_code_reviewer() -> MockCodeReviewer:
#     """Crea un code reviewer mock."""
#     return MockCodeReviewer()


# @pytest.fixture
# def mock_github_client() -> MockGitHubAdapter:
#     """Crea un cliente GitHub mock."""
#     return MockGitHubAdapter()
