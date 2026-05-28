from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ReviewResult:
    """Resultado de una revision de codigo."""
    
    rating: int
    summary: str
    recommendations: list[str]

@dataclass
class CodeContent:
    """Contenido del codigo a revisar."""
    
    files: dict[str, str] # {filepath: content}
    folder_structure: list[str]
    pr_title: str
    pr_description: str

class ICodeReviewer(ABC):
    """Interface abstracta para el revisor de codigo basado en IA."""

    @abstractmethod
    def review_code(self, code: CodeContent) -> ReviewResult:
        """Evalua el codigo y retorna calificacion con recomendaciones."""
        ...

    @abstractmethod
    def get_review_rules(self) -> list[str]:
        """Retorna las reglas predefinidas usadas para evaluar el codigo."""
        ...