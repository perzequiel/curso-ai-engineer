"""Clase 5: Tests para SendReviewUseCase.

Verifica la orquestacion completa del proceso de revision:
obtener PR, revisar codigo y almacenar resultado.
"""

import pytest

from src.application.use_cases.send_review import SendReviewUseCase
from src.domain.value_objects.review_status import ReviewStatus
from src.infrastructure.ai.ai_code_reviewer import MockCodeReviewer
from src.infrastructure.github.github_adapter import MockGitHubAdapter
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository


class TestSendReviewUseCase:
    """Tests para el caso de uso de enviar revision."""

    def setup_method(self):
        self.repository = InMemoryReviewRepository()
        self.code_reviewer = MockCodeReviewer(default_rating=85)
        self.github_client = MockGitHubAdapter()
        self.use_case = SendReviewUseCase(
            review_repository=self.repository,
            code_reviewer=self.code_reviewer,
            github_client=self.github_client,
        )

    def test_execute_successful_review(self):
        review = self.use_case.execute(pr_id="1")
        assert review.status == ReviewStatus.COMPLETED
        assert review.rating is not None
        assert review.summary != ""
        assert len(review.recommendations) > 0

    def test_execute_stores_review_in_repository(self):
        review = self.use_case.execute(pr_id="1")
        stored = self.repository.find_by_id(review.id)
        assert stored is not None
        assert stored.id == review.id

    def test_execute_with_nonexistent_pr_fails(self):
        review = self.use_case.execute(pr_id="999")
        assert review.status == ReviewStatus.FAILED
        assert "not found" in review.summary.lower()

    def test_execute_approved_review(self):
        self.code_reviewer = MockCodeReviewer(default_rating=90)
        use_case = SendReviewUseCase(
            review_repository=self.repository,
            code_reviewer=self.code_reviewer,
            github_client=self.github_client,
        )
        review = use_case.execute(pr_id="1")
        assert review.is_approved() is True

    def test_execute_rejected_review(self):
        self.code_reviewer = MockCodeReviewer(default_rating=30)
        use_case = SendReviewUseCase(
            review_repository=self.repository,
            code_reviewer=self.code_reviewer,
            github_client=self.github_client,
        )
        review = use_case.execute(pr_id="1")
        assert review.is_approved() is False

    def test_execute_sets_pr_id_on_review(self):
        review = self.use_case.execute(pr_id="2")
        assert review.pr_id == "2"
