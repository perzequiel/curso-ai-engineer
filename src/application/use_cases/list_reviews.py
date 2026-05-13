from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class ListReviewsUseCase:
    def __init__(self, review_repository: IReviewRepository):
        self._review_repository = review_repository

    def execute(self) -> list[Review]:
        return self._review_repository.find_all()
