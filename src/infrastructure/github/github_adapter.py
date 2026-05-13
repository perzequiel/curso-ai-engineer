from github import Github

from src.domain.ports.github_client import IGitHubClient, PRFile, PRInfo


class GitHubAdapter(IGitHubClient):
    def __init__(self, token: str, repo_name: str):
        self._token = token
        self._repo_name = repo_name

    def get_pr_code(self, pr_id: str) -> PRInfo:
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)
        pr = repo.get_pull(int(pr_id))

        files = self.get_pr_files(pr_id)
        folder_structure = sorted(
            {f.filename.rsplit("/", 1)[0] for f in files if "/" in f.filename}
        )

        return PRInfo(
            pr_id=pr_id,
            title=pr.title,
            description=pr.body or "",
            author=pr.user.login,
            files=files,
            folder_structure=folder_structure,
        )

    def get_pr_files(self, pr_id: str) -> list[PRFile]:
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

    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        g = Github(self._token)
        repo = g.get_repo(self._repo_name)
        pr = repo.get_pull(int(pr_id))
        pr.create_issue_comment(comment)
        return True


class MockGitHubAdapter(IGitHubClient):
    def __init__(self):
        self._mock_prs: dict[str, PRInfo] = {
            "1": PRInfo(
                pr_id="1",
                title="Test PR",
                description="Test description",
                author="testuser",
                files=[
                    PRFile(
                        filename="src/main.py",
                        content="def main(): pass",
                        status="added",
                        patch="+def main(): pass",
                    )
                ],
                folder_structure=["src"],
            ),
            "2": PRInfo(
                pr_id="2",
                title="Another PR",
                description="",
                author="testuser",
                files=[],
                folder_structure=[],
            ),
        }

    def get_pr_code(self, pr_id: str) -> PRInfo:
        if pr_id not in self._mock_prs:
            raise ValueError(f"PR {pr_id} not found")
        return self._mock_prs[pr_id]

    def get_pr_files(self, pr_id: str) -> list[PRFile]:
        return self.get_pr_code(pr_id).files

    def post_review_comment(self, pr_id: str, comment: str) -> bool:
        return True
