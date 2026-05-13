from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class ReviewNotFoundError(Exception):
    pass


class GetReviewResultUseCase:
    def __init__(self, review_repository: IReviewRepository):
        self._review_repository = review_repository

    def execute(self, pr_id: str) -> Review:
        review = self._review_repository.find_by_pr_id(pr_id)
        if review is None:
            raise ReviewNotFoundError(f"Review for PR '{pr_id}' not found")
        return review
