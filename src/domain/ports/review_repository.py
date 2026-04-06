from abc import ABC, abstractmethod

class IReviewRepository(ABC):
    """ repo """

    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def find_by_pr_id(self):
        pass
    
    @abstractmethod
    def find_by_id(self):
        pass

    @abstractmethod
    def find_all(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass