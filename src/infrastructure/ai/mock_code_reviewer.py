"""MockCodeReviewer - Mock de revision de codigo para testing y demos.

No depende de LangChain ni de Claude. Simula una revision basica
inspeccionando los archivos del PR.
"""
from src.domain.ports.code_reviewer import CodeContent, ICodeReviewer, ReviewResult
from src.infrastructure.ai.review_rules import DEFAULT_REVIEW_RULES


class MockCodeReviewer(ICodeReviewer):
    """Revisor de codigo mock para testing y demostraciones."""

    def __init__(self, default_rating: int = 85):
        self._default_rating = default_rating
        self._rules = DEFAULT_REVIEW_RULES

    def review_code(self, code: CodeContent) -> ReviewResult:
        """Simula una revision de codigo."""
        num_files = len(code.files)
        has_tests = any("test" in f.lower() for f in code.files)

        rating = self._default_rating
        if not has_tests:
            rating -= 15

        recommendations = [
            "Consider adding more unit tests for edge cases",
            "Add type hints to function parameters",
        ]

        if num_files > 5:
            recommendations.append("Consider splitting into smaller PRs")
            rating -= 5

        return ReviewResult(
            rating=max(0, min(100, rating)),
            summary=f"Code review of {num_files} files. "
            f"{'Includes tests.' if has_tests else 'Missing tests.'}",
            recommendations=recommendations,
        )

    def get_review_rules(self) -> list[str]:
        """Retorna las reglas de revision."""
        return self._rules.copy()
