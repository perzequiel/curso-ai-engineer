from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class CodeContent:
    "Contenido del codigo a revisar"

    files: dict[str, str]
    folder_structure: list[str]
    pr_title: str
    pr_description: str


@dataclass
class ReviewResult:
    "Resultado de una revision de codigo"

    rating: int
    summary: str
    recommendations: list[str]


class ICodeReviewer(ABC):

    @abstractmethod
    def review_code(code: CodeContent) -> ReviewResult:
        pass

    @abstractmethod
    def get_review_rules() -> list[str]:
        pass
