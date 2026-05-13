"""GitHubAdapter - Adaptador para la API de GitHub.

Implementacion concreta del puerto IGitHubClient usando PyGithub.
"""

from github import Github

from src.domain.ports.github_client import IGitHubClient, PRFile, PRInfo, PRSummary


class GitHubAdapter(IGitHubClient):
    """Adaptador que conecta con la API de GitHub via PyGithub."""

    def __init__(self, token: str, repo_name: str):
        self._token = token
        self._repo_name = repo_name

    def get_pr_code(self, pr_id: str) -> PRInfo:
        """Obtiene toda la informacion y codigo de un Pull Request."""
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)
        pr = repo.get_pull(int(pr_id))

        files = self.get_pr_files(pr_id)
        folder_structure = sorted({f.filename.rsplit("/", 1)[0] for f in files if "/" in f.filename})

        return PRInfo(
            pr_id=pr_id,
            title=pr.title,
            description=pr.body or "",
            author=pr.user.login,
            files=files,
            folder_structure=folder_structure,
        )

    def get_pr_files(self, pr_id: str) -> list[PRFile]:
        """Obtiene la lista de archivos modificados en un PR."""
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)
        pr = repo.get_pull(int(pr_id))

        return [
            PRFile(
                filename=f.filename,
                content=f.patch or "",
                status=f.status,
                patch=f.patch or "",
            )
            for f in pr.get_files()
        ]

    def list_prs(self, state: str = "open") -> list[PRSummary]:
        """Lista los PRs del repositorio configurado.

        PyGithub acepta state="open" | "closed" | "all".
        """
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)

        return [
            PRSummary(
                pr_id=str(pr.number),
                title=pr.title,
                description=pr.body or "",
                author=pr.user.login,
                state=pr.state,
                url=pr.html_url,
            )
            for pr in repo.get_pulls(state=state)
        ]

    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        """Publica un comentario de revision en el PR."""
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)
        pr = repo.get_pull(int(pr_id))
        pr.create_issue_comment(comment)
        return True
