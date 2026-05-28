from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PRFile:
    """Representa un archivo de un Pull Request."""

    filename: str
    content: str
    status: str 
    patch: str

@dataclass
class PRInfo:
    """Informacion de un Pull Request."""

    pr_id: str
    title: str
    description: str
    author: str
    files: list[PRFile]
    folder_structure: list[str]

class IGitHubClient(ABC):
    """Interface abstracta para interaccion con GitHub."""

    @abstractmethod
    def get_pr_code(self, pr_id: str) -> PRInfo:
        """Obtiene toda la informacion y codigo de un Pull Request."""
        ...

    @abstractmethod
    def get_pr_files(self, pr_id: str) -> list[PRFile]:
        """Obtiene la lista de archivos modificados en un PR."""
        ...

    @abstractmethod
    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        """Publica un comentario de revision en el PR."""
        ...