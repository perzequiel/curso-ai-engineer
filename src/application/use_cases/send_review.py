"""Clase 5: SendReviewUseCase - Caso de uso para enviar una revision.

Orquesta el proceso de enviar un Pull Request para revision:
1. Obtiene el codigo del PR via GitHub
2. Envia el codigo al CodeReviewer (agente IA)
3. Almacena la revision en el repositorio
"""

from src.domain.entities.review import Review
from src.domain.ports.code_reviewer import CodeContent, ICodeReviewer
from src.domain.ports.github_client import IGitHubClient
from src.domain.ports.review_repository import IReviewRepository
from src.domain.value_objects.rating import Rating


class SendReviewUseCase:
    """Caso de uso: enviar un PR para revision de codigo."""

    def __init__(
        self,
        review_repository: IReviewRepository,
        code_reviewer: ICodeReviewer,
        github_client: IGitHubClient,
    ):
        self._review_repository = review_repository
        self._code_reviewer = code_reviewer
        self._github_client = github_client

    def execute(self, pr_id: str) -> Review:
        """Ejecuta el proceso completo de revision de un PR.

        Args:
            pr_id: ID del Pull Request a revisar.

        Returns:
            Review con los resultados de la revision.
        """
        review = Review(pr_id=pr_id)
        review.start_processing()
        self._review_repository.save(review)

        try:
            pr_info = self._github_client.get_pr_code(pr_id)

            code_content = CodeContent(
                files={f.filename: f.content for f in pr_info.files},
                folder_structure=pr_info.folder_structure,
                pr_title=pr_info.title,
                pr_description=pr_info.description,
            )

            result = self._code_reviewer.review_code(code_content)

            rating = Rating(result.rating)
            review.complete(
                rating=rating,
                summary=result.summary,
                recommendations=result.recommendations,
            )
        except Exception as e:
            review.fail(str(e))

        self._review_repository.save(review)
        return review
