
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class PRFile:
    """Representa un archivo de un Pull Request"""
    filename: str
    content: str
    status: str
    patch: str
    
@dataclass
class PRInfo:
    """Informacion de un Pull Request"""
    pr_id: str
    title: str
    description: str
    author: str
    files: list[PRFile]
    folder_structure: list[str]

class IGitHubClient(ABC):
    """Interface abstracta para una interaccion con Github"""
    @abstractmethod
    
    def get_pr_code(self) -> PRFile:
        """OBtiene toda la informacion y codigo de una Pull Request"""
        pass
    
    @abstractmethod
    def get_pr_files(self) -> list[PRFile]:
        """Obtiene la lista de de archivos modificados de una PR"""
        pass
    
    @abstractmethod
    def post_review_comment(self) -> bool:
        """Publica un comentario de revision en el PR"""
        pass
    

