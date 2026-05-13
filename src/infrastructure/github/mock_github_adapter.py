"""MockGitHubAdapter - Mock de GitHub para testing y demos.

No depende de PyGithub. Sirve datos fijos en memoria simulando un repo.
"""
from src.domain.ports.github_client import IGitHubClient, PRFile, PRInfo, PRSummary


class MockGitHubAdapter(IGitHubClient):
    """Adaptador mock de GitHub para testing y demostraciones."""

    def __init__(self) -> None:
        self._mock_prs: dict[str, PRInfo] = {
            "1": PRInfo(
                pr_id="1",
                title="Add user authentication",
                description="Implements JWT-based authentication for the API",
                author="dev-student",
                files=[
                    PRFile(
                        filename="src/auth/jwt_handler.py",
                        content='import jwt\n\ndef create_token(user_id: str) -> str:\n    return jwt.encode({"user_id": user_id}, "secret")\n',
                        status="added",
                        patch="+ import jwt\n+ def create_token...",
                    ),
                    PRFile(
                        filename="src/auth/middleware.py",
                        content='def auth_middleware(request):\n    token = request.headers.get("Authorization")\n    if not token:\n        raise ValueError("No token")\n',
                        status="added",
                        patch="+ def auth_middleware...",
                    ),
                ],
                folder_structure=["src/auth"],
            ),
            "2": PRInfo(
                pr_id="2",
                title="Fix database connection pool",
                description="Fixes connection leak in the DB pool manager",
                author="senior-dev",
                files=[
                    PRFile(
                        filename="src/db/pool.py",
                        content='class ConnectionPool:\n    def __init__(self, max_size=10):\n        self.max_size = max_size\n        self._connections = []\n\n    def acquire(self):\n        if self._connections:\n            return self._connections.pop()\n        return self._create_connection()\n\n    def release(self, conn):\n        if len(self._connections) < self.max_size:\n            self._connections.append(conn)\n        else:\n            conn.close()\n',
                        status="modified",
                        patch="- self._connections = []\n+ self._connections: list = []",
                    ),
                ],
                folder_structure=["src/db"],
            ),
        }

    def get_pr_code(self, pr_id: str) -> PRInfo:
        """Retorna datos mock de un PR."""
        if pr_id not in self._mock_prs:
            raise ValueError(f"Mock PR '{pr_id}' not found")
        return self._mock_prs[pr_id]

    def get_pr_files(self, pr_id: str) -> list[PRFile]:
        """Retorna archivos mock de un PR."""
        pr_info = self.get_pr_code(pr_id)
        return pr_info.files

    def list_prs(self, state: str = "open") -> list[PRSummary]:
        """Retorna un listado mock de PRs (ignora el filtro de estado)."""
        return [
            PRSummary(
                pr_id=pr.pr_id,
                title=pr.title,
                description=pr.description,
                author=pr.author,
                state="open",
                url=f"https://github.com/mock/repo/pull/{pr.pr_id}",
            )
            for pr in self._mock_prs.values()
        ]

    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        """Simula publicar un comentario."""
        return True
