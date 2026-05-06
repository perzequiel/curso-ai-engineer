from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PRFile:
    filename: str
    content: str
    status: str  #added, modified, removed
    patch: str

@dataclass
class PRInfo:
    pr_id: str
    title: str
    description: str
    author: str
    files: list[PRFile]
    folder_structure: list[str]

class IGithubClient(ABC):
    @abstractmethod
    def get_pr_code(self, pr_id: str) -> PRInfo:
        """Obtiene toda la informacion y codigo de un Pull Request."""

    @abstractmethod
    def get_pr_files(self, pr_id: str) -> list[PRFile]:
        """Obtiene la lista de archivos modificados en un PR"""

    @abstractmethod
    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        """Publica un comentario de revision en el PR"""