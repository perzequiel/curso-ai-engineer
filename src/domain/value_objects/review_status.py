"""Value Object: ReviewStatus - Estados posibles de una revision."""

from enum import Enum


class ReviewStatus(Enum):
    """Estados posibles de una revision de codigo."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
