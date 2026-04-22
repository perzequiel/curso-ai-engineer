from abc import ABC, abstractmethod

from src.domain.entities.review import Review

class IReviewRepository(ABC):

    @abstractmethod
    def save(self, review: Review) -> Review:
        pass

    @abstractmethod
    def find_by_pr_id(self, pr_id: str) -> Review | None:
        pass

    @abstractmethod
    def find_by_id(self, review_id: str) -> Review | None:
        pass

    @abstractmethod
    def find_all(self) -> list[Review]:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
