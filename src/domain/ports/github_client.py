from abc import ABC, abstractmethod
from dataclasses import dataclass
from src.domain.entities.review import Review

@dataclass
class PRFile:
    filename: str 
    content: str 
    status: str 
    patch: str

@dataclass
class PRInfo:
    pr_id: str 
    title: str 
    description: str 
    author: str
    files: list[PRFile]
    folder_structure: list[str]

class IGitHubClient(ABC):
    @abstractmethod
    def get_pr_code(self, pr_id: str) -> PRInfo:
        """ get_pr_code """

    @abstractmethod
    def get_pr_files(self, pr_id: str) -> list[PRInfo]:
        """ get_pr_code """    

    @abstractmethod
    def post_review_comment(self, pr_id: str, comment: str) -> bool:   
        """ post_review_comment """  