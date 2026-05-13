from src.domain.entities.review import Review
from src.domain.ports.review_repository import IReviewRepository


class InMemoryReviewRepository(IReviewRepository):
    def __init__(self):
        self._reviews: dict[str, Review] = {}

    def save(self, review: Review) -> Review:
        self._reviews[review.id] = review
        return review

    def find_by_pr_id(self, pr_id: str) -> Review | None:
        for review in self._reviews.values():
            if review.pr_id == pr_id:
                return review
        return None

    def find_by_id(self, review_id: str) -> Review | None:
        return self._reviews.get(review_id)

    def find_all(self) -> list[Review]:
        return sorted(self._reviews.values(), key=lambda r: r.created_at)

    def delete(self, review_id: str) -> bool:
        if review_id in self._reviews:
            del self._reviews[review_id]
            return True
        return False

    def clear(self) -> None:
        self._reviews.clear()
