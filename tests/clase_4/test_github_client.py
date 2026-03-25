"""Clase 4: Tests para el puerto IGitHubClient.

Verifica la interface abstracta del cliente GitHub
y los dataclasses asociados (PRFile, PRInfo).
"""

from abc import ABC

import pytest

from src.domain.ports.github_client import IGitHubClient, PRFile, PRInfo


class TestIGitHubClientInterface:
    """Tests para verificar la interface del cliente GitHub."""

    def test_is_abstract_class(self):
        assert issubclass(IGitHubClient, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            IGitHubClient()

    def test_defines_get_pr_code_method(self):
        assert hasattr(IGitHubClient, "get_pr_code")

    def test_defines_get_pr_files_method(self):
        assert hasattr(IGitHubClient, "get_pr_files")

    def test_defines_post_review_comment_method(self):
        assert hasattr(IGitHubClient, "post_review_comment")


class TestPRFile:
    """Tests para el dataclass PRFile."""

    def test_create_pr_file(self):
        pr_file = PRFile(
            filename="src/main.py",
            content="print('hello')",
            status="added",
            patch="+ print('hello')",
        )
        assert pr_file.filename == "src/main.py"
        assert pr_file.content == "print('hello')"
        assert pr_file.status == "added"
        assert pr_file.patch == "+ print('hello')"

    def test_pr_file_status_types(self):
        for status in ["added", "modified", "removed"]:
            pr_file = PRFile(
                filename="test.py",
                content="",
                status=status,
                patch="",
            )
            assert pr_file.status == status


class TestPRInfo:
    """Tests para el dataclass PRInfo."""

    def test_create_pr_info(self):
        files = [
            PRFile(filename="main.py", content="code", status="added", patch="+code"),
        ]
        pr_info = PRInfo(
            pr_id="42",
            title="Add feature",
            description="Implements new feature",
            author="dev",
            files=files,
            folder_structure=["src"],
        )
        assert pr_info.pr_id == "42"
        assert pr_info.title == "Add feature"
        assert pr_info.author == "dev"
        assert len(pr_info.files) == 1
        assert pr_info.folder_structure == ["src"]

    def test_pr_info_with_no_files(self):
        pr_info = PRInfo(
            pr_id="1",
            title="Empty PR",
            description="",
            author="dev",
            files=[],
            folder_structure=[],
        )
        assert len(pr_info.files) == 0
