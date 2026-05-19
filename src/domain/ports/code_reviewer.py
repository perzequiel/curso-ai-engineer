from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ReviewResult:
    rating: int
    summary: str
    recommendations: list[str]


@dataclass
class CodeContent:
    files: dict[str, str]
    folder_structure: list[str]
    pr_title: str
    pr_description: str


class ICodeReviewer(ABC):
    @abstractmethod
    def review_code(self, code: CodeContent) -> ReviewResult: pass

    @abstractmethod
    def get_review_rules(self) -> list[str]: 
        return self._rules


