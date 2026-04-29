from abc import ABC, abstractmethod

from src.domain.entities.review import Review


class IReviewRepository(ABC):
    """repo"""

    @abstractmethod
    def save(review: Review) -> Review:
        pass

    @abstractmethod
    def find_by_pr_id(pr_id: str) -> Review | None:
        pass

    @abstractmethod
    def find_by_id(review_id: str) -> Review | None:
        pass

    @abstractmethod
    def find_all() -> list[Review]:
        pass

    @abstractmethod
    def delete(review_id: str) -> bool:
        pass
