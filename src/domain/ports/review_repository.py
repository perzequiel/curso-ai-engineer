from abc import ABC, abstractmethod
from src.domain.entities.review import Review

class IReviewRepository(ABC):
    @abstractmethod
    def save(self, review: Review) -> Review:
        """ save """
    @abstractmethod
    def find_by_pr_id(self, pr_id: str) -> Review | None:
        """ find_by_pr_id """
    @abstractmethod
    def find_by_id(self, review_id: str) -> Review | None:
        """ find_by_id """
    @abstractmethod
    def find_all(self) -> list[Review]:
        """ find_all """
    @abstractmethod
    def delete(self, review_id: str) -> bool:
        """ delete """