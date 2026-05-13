// Types based on the FastAPI backend (see src/infrastructure/api/http_api.py).

export interface PRSummaryResponse {
  pr_id: string
  title: string
  description: string
  author: string
  // Backend returns the raw GitHub state ("open" | "closed"); we keep it as
  // a string to also tolerate other values (e.g. "merged").
  state: string
  url: string
}

export type ReviewStatus = "pending" | "in_progress" | "completed" | "failed"

export interface ReviewResponse {
  id: string
  pr_id: string
  status: ReviewStatus
  // Rating is 0-100 (matches domain Rating value object).
  rating: number | null
  summary: string
  recommendations: string[]
  approved: boolean
}

export interface ReviewRequest {
  pr_id: string
}

// Query param accepted by GET /prs?state=...
export type PRState = "open" | "closed" | "all"

export interface PRWithReviewStatus extends PRSummaryResponse {
  hasReview: boolean
  review?: ReviewResponse
}
