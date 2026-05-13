import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from src.application.use_cases.get_review_result import (
    GetReviewResultUseCase,
    ReviewNotFoundError,
)
from src.application.use_cases.list_reviews import ListReviewsUseCase
from src.application.use_cases.send_review import SendReviewUseCase
from src.domain.entities.review import Review
from src.infrastructure.ai.ai_code_reviewer import AICodeReviewer, MockCodeReviewer
from src.infrastructure.github.github_adapter import GitHubAdapter, MockGitHubAdapter
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository

load_dotenv()

app = FastAPI(title="Code Review API")

_repository = InMemoryReviewRepository()


def _build_github_client():
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if token and repo:
        return GitHubAdapter(token=token, repo_name=repo)
    return MockGitHubAdapter()


def _build_code_reviewer():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return AICodeReviewer(api_key=api_key)
    return MockCodeReviewer(default_rating=85)


def get_send_review() -> SendReviewUseCase:
    return SendReviewUseCase(
        review_repository=_repository,
        code_reviewer=_build_code_reviewer(),
        github_client=_build_github_client(),
    )


def get_get_review() -> GetReviewResultUseCase:
    return GetReviewResultUseCase(review_repository=_repository)


def get_list_reviews() -> ListReviewsUseCase:
    return ListReviewsUseCase(review_repository=_repository)


class ReviewRequest(BaseModel):
    pr_id: str


class ReviewResponse(BaseModel):
    id: str
    pr_id: str
    status: str
    rating: int | None
    summary: str
    recommendations: list[str]
    approved: bool

    @classmethod
    def from_entity(cls, review: Review) -> "ReviewResponse":
        return cls(
            id=review.id,
            pr_id=review.pr_id,
            status=review.status.value,
            rating=review.rating.value if review.rating else None,
            summary=review.summary,
            recommendations=review.recommendations,
            approved=review.is_approved(),
        )


@app.post("/reviews", response_model=ReviewResponse, status_code=201)
def create_review(
    body: ReviewRequest,
    use_case: SendReviewUseCase = Depends(get_send_review),
) -> ReviewResponse:
    review = use_case.execute(pr_id=body.pr_id)
    return ReviewResponse.from_entity(review)


@app.get("/reviews/{pr_id}", response_model=ReviewResponse)
def get_review(
    pr_id: str,
    use_case: GetReviewResultUseCase = Depends(get_get_review),
) -> ReviewResponse:
    try:
        review = use_case.execute(pr_id=pr_id)
    except ReviewNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return ReviewResponse.from_entity(review)


@app.get("/reviews", response_model=list[ReviewResponse])
def list_reviews(
    use_case: ListReviewsUseCase = Depends(get_list_reviews),
) -> list[ReviewResponse]:
    return [ReviewResponse.from_entity(r) for r in use_case.execute()]
