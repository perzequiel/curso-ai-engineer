"""ListPRsUseCase - Caso de uso para listar PRs disponibles del repositorio.

Consulta el puerto IGitHubClient para obtener un resumen de los Pull
Requests del repo configurado, sin descargar el contenido de los archivos.
"""

from src.domain.ports.github_client import IGitHubClient, PRSummary


class ListPRsUseCase:
    """Caso de uso: listar los Pull Requests del repositorio configurado."""

    def __init__(self, github_client: IGitHubClient):
        self._github_client = github_client

    def execute(self, state: str = "open") -> list[PRSummary]:
        """Lista los PRs filtrando por estado.

        Args:
            state: "open", "closed" o "all".

        Returns:
            Lista de resumenes de PRs.
        """
        return self._github_client.list_prs(state=state)
