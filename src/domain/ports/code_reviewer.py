from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CodeContent():
    files: dict[str, str]
    folder_structure: list[str]
    pr_title: str
    pr_description: str

@dataclass
class ReviewResult():
    rating: int
    summary: str
    recommendations: list[str]



class ICodeReviewer(ABC):

    @abstractmethod
    def review_code(self, code: CodeContent) -> ReviewResult:
        pass

    @abstractmethod
    def get_review_rules(self) -> list[str]:
        pass