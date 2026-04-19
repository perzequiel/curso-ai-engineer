from abc import ABC, abstractmethod

from src.domain.entities.review import Review

class IReviewRepository(ABC):
    @abstractmethod
    def save(self, review: Review) -> Review:
        None

    @abstractmethod
    def find_by_pr_id(self) -> Review:
        None

    @abstractmethod
    def find_by_id(self) -> Review:
        None

    @abstractmethod
    def find_all(self) -> list[Review]:
        None
        
    @abstractmethod
    def delete(self) -> bool:
        None