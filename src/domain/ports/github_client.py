"""Clase 4: IGitHubClient - Puerto para interaccion con GitHub API.

Define la interface abstracta para obtener informacion de
Pull Requests y publicar comentarios de revision.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PRFile:
    """Representa un archivo de un Pull Request."""

    filename: str
    content: str
    status: str  # added, modified, removed
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


@dataclass
class PRSummary:
    """Resumen liviano de un Pull Request (sin contenido de archivos)."""

    pr_id: str
    title: str
    description: str
    author: str
    state: str  # open, closed
    url: str


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
    def list_prs(self, state: str = "open") -> list[PRSummary]:
        """Lista los Pull Requests del repositorio.

        Args:
            state: Filtro de estado: "open", "closed" o "all".

        Returns:
            Lista de resumenes de PRs (sin contenido de archivos).
        """
        ...

    @abstractmethod
    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        """Publica un comentario de revision en el PR."""
        ...
