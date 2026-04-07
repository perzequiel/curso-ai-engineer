from abc import ABC, abstractmethod
from src.domain.entities.review import Review

class IReviewRepository(ABC):
    @abstractmethod 
    def save( self, review: Review) -> Review:
        return True
   
    @abstractmethod 
    def find_by_pr_id(self, pr_id: str) -> (Review | None): 
        return True
    
    @abstractmethod 
    def find_by_id(self, review_id: str) -> (Review | None): 
        return True
    
    @abstractmethod
    def find_all(self) -> list[Review]: 
        return True
    
    @abstractmethod
    def delete(self, review_id: str) -> bool: 
        return True