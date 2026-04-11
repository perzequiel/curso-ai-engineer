from dataclasses import dataclass
from abc import ABC, abstractmethod

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
    autor: str
    files: list[PRFile]
    folder_estructure: list[str]
    
class ICodeCliente(ABC):
    @abstractmethod
    def get_pr_code(self, pr_id: str)-> PRInfo:
        pass
    @abstractmethod
    def get_pr_files(self, pr_id: str)-> list[PRFile]:
        pass
    @abstractmethod
    def post_review_comment(self, pr_id: str, comment: str)-> bool:
        pass
    