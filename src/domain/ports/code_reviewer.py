from abc import ABC, abstractmethod

class ICodeReviewer(ABC):
    
    @abstractmethod
    def review_code(self):
        pass
    @abstractmethod
    def get_review_rules(self):
        pass

from dataclasses import dataclass


@dataclass
class CodeContent:
    "Content to be review"

    files: dict[str, str]
    folder_structure: list[str]
    pr_title: str
    pr_description: str

@dataclass
class ReviewResult:
    "Result"

    rating: int
    summary: str
    recommendations: list[str]