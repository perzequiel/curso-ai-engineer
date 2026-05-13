from src.domain.entities.review import Review
from src.domain.ports.code_reviewer import ICodeReviewer, CodeContent
from src.domain.ports.github_client import IGitHubClient
from src.domain.ports.review_repository import IReviewRepository
from src.domain.value_objects.rating import Rating


class SendReviewUseCase:
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
        review = Review(pr_id=pr_id)
        review.start_processing()
        self._review_repository.save(review)

        try:
            pr_info = self._github_client.get_pr_code(pr_id)
        except Exception as e:
            review.fail(str(e))
            self._review_repository.save(review)
            return review

        code = CodeContent(
            files={f.filename: f.content for f in pr_info.files},
            folder_structure=pr_info.folder_structure,
            pr_title=pr_info.title,
            pr_description=pr_info.description,
        )

        try:
            result = self._code_reviewer.review_code(code)
        except Exception as e:
            review.fail(str(e))
            self._review_repository.save(review)
            return review

        review.complete(
            rating=Rating(result.rating),
            summary=result.summary,
            recommendations=result.recommendations,
        )
        self._review_repository.save(review)
        return review
