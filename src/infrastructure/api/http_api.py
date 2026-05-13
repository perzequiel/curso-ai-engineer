"""API HTTP para disparar revisiones de PRs."""

import os

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.application.use_cases.get_review_result import (
    GetReviewResultUseCase,
    ReviewNotFoundError,
)
from src.application.use_cases.list_prs import ListPRsUseCase
from src.application.use_cases.list_reviews import ListReviewsUseCase
from src.application.use_cases.send_review import SendReviewUseCase
from src.domain.entities.review import Review
from src.domain.ports.github_client import PRSummary
from src.infrastructure.ai.ai_code_reviewer import AICodeReviewer
from src.infrastructure.ai.mock_code_reviewer import MockCodeReviewer
from src.infrastructure.github.github_adapter import GitHubAdapter
from src.infrastructure.github.mock_github_adapter import MockGitHubAdapter
from src.infrastructure.persistence.in_memory_repository import InMemoryReviewRepository

load_dotenv()

app = FastAPI(title="Code Review API")

_default_cors_origins = "http://localhost:3000,http://127.0.0.1:3000"
_cors_origins = [
    origin.strip()
    for origin in os.environ.get("CORS_ORIGINS", _default_cors_origins).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_repository = InMemoryReviewRepository()
# _repository = DBReviewRepository()


def _build_github_client():
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPO")
    if token and repo:
        return GitHubAdapter(token=token, repo_name=repo)
    return MockGitHubAdapter()


def _build_code_reviewer():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
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


def get_list_prs() -> ListPRsUseCase:
    return ListPRsUseCase(github_client=_build_github_client())


class ReviewRequest(BaseModel):
    pr_id: str


class PRSummaryResponse(BaseModel):
    pr_id: str
    title: str
    description: str
    author: str
    state: str
    url: str

    @classmethod
    def from_summary(cls, pr: PRSummary) -> "PRSummaryResponse":
        return cls(
            pr_id=pr.pr_id,
            title=pr.title,
            description=pr.description,
            author=pr.author,
            state=pr.state,
            url=pr.url,
        )


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


@app.get("/prs", response_model=list[PRSummaryResponse])
def list_prs(
    state: str = "open",
    use_case: ListPRsUseCase = Depends(get_list_prs),
) -> list[PRSummaryResponse]:
    """Lista los PRs del repositorio configurado en GITHUB_REPO.

    Query params:
        state: "open" (default), "closed" o "all".
    """
    return [PRSummaryResponse.from_summary(pr) for pr in use_case.execute(state=state)]
