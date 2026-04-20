
from abc import ABC, abstractmethod
from dataclasses import dataclass

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
    def get_pr_code(self) -> PRFile:
        pass
    
    @abstractmethod
    def get_pr_files(self) -> list[PRFile]:
        pass
    
    @abstractmethod
    def post_review_comment(self) -> bool:
        pass
    

