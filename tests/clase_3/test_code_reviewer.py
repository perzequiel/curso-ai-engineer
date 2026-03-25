"""Clase 3: Tests para el puerto ICodeReviewer.

Verifica la interface abstracta del revisor de codigo
y los dataclasses asociados (ReviewResult, CodeContent).
"""

from abc import ABC

import pytest

from src.domain.ports.code_reviewer import (
    CodeContent,
    ICodeReviewer,
    ReviewResult,
)


class TestICodeReviewerInterface:
    """Tests para verificar la interface del code reviewer."""

    def test_is_abstract_class(self):
        assert issubclass(ICodeReviewer, ABC)

    def test_cannot_instantiate_directly(self):
        with pytest.raises(TypeError):
            ICodeReviewer()

    def test_defines_review_code_method(self):
        assert hasattr(ICodeReviewer, "review_code")

    def test_defines_get_review_rules_method(self):
        assert hasattr(ICodeReviewer, "get_review_rules")


class TestReviewResult:
    """Tests para el dataclass ReviewResult."""

    def test_create_review_result(self):
        result = ReviewResult(
            rating=85,
            summary="Good code",
            recommendations=["Add tests"],
        )
        assert result.rating == 85
        assert result.summary == "Good code"
        assert result.recommendations == ["Add tests"]

    def test_review_result_with_empty_recommendations(self):
        result = ReviewResult(rating=50, summary="Needs work", recommendations=[])
        assert result.recommendations == []


class TestCodeContent:
    """Tests para el dataclass CodeContent."""

    def test_create_code_content(self):
        content = CodeContent(
            files={"main.py": "print('hello')"},
            folder_structure=["src"],
            pr_title="Add feature",
            pr_description="New feature implementation",
        )
        assert content.files == {"main.py": "print('hello')"}
        assert content.folder_structure == ["src"]
        assert content.pr_title == "Add feature"
        assert content.pr_description == "New feature implementation"

    def test_code_content_with_multiple_files(self):
        content = CodeContent(
            files={
                "src/main.py": "import utils",
                "src/utils.py": "def helper(): pass",
            },
            folder_structure=["src"],
            pr_title="Refactor",
            pr_description="Code cleanup",
        )
        assert len(content.files) == 2
