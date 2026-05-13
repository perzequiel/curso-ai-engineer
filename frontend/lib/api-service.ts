import type {
  PRSummaryResponse,
  ReviewResponse,
  ReviewRequest,
  PRState,
  PRWithReviewStatus,
} from "./types"

// Base URL of the FastAPI backend. Override with NEXT_PUBLIC_API_URL in
// frontend/.env.local for production / different hosts.
const API_BASE_URL = (
  process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "")

export class ApiError extends Error {
  readonly status: number
  readonly url: string

  constructor(status: number, url: string, message: string) {
    super(message)
    this.name = "ApiError"
    this.status = status
    this.url = url
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${API_BASE_URL}${path}`
  let response: Response
  try {
    response = await fetch(url, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init?.body ? { "Content-Type": "application/json" } : {}),
        ...(init?.headers ?? {}),
      },
    })
  } catch (cause) {
    throw new ApiError(
      0,
      url,
      `No se pudo contactar la API en ${API_BASE_URL}. ¿Está corriendo FastAPI?`,
    )
  }

  if (!response.ok) {
    let detail = response.statusText
    try {
      const body = await response.json()
      if (body && typeof body === "object" && "detail" in body) {
        detail = String((body as { detail: unknown }).detail)
      }
    } catch {
      // ignore JSON parse errors, keep statusText
    }
    throw new ApiError(response.status, url, detail)
  }

  if (response.status === 204) {
    return undefined as unknown as T
  }
  return (await response.json()) as T
}

export const apiService = {
  // GET /prs?state=...
  async listPRs(state: PRState = "open"): Promise<PRSummaryResponse[]> {
    const query = new URLSearchParams({ state }).toString()
    return request<PRSummaryResponse[]>(`/prs?${query}`)
  },

  // GET /reviews
  async listReviews(): Promise<ReviewResponse[]> {
    return request<ReviewResponse[]>("/reviews")
  },

  // GET /reviews/{pr_id} — returns null when the backend responds 404.
  async getReview(prId: string): Promise<ReviewResponse | null> {
    try {
      return await request<ReviewResponse>(
        `/reviews/${encodeURIComponent(prId)}`,
      )
    } catch (error) {
      if (error instanceof ApiError && error.status === 404) {
        return null
      }
      throw error
    }
  },

  // POST /reviews
  async createReview(body: ReviewRequest): Promise<ReviewResponse> {
    return request<ReviewResponse>("/reviews", {
      method: "POST",
      body: JSON.stringify(body),
    })
  },

  // Convenience: list PRs and join them with their (optional) review.
  async getPRsWithReviewStatus(
    state: PRState = "open",
  ): Promise<PRWithReviewStatus[]> {
    const [prs, reviews] = await Promise.all([
      this.listPRs(state),
      this.listReviews(),
    ])

    const reviewMap = new Map(reviews.map((r) => [r.pr_id, r]))

    return prs.map((pr) => ({
      ...pr,
      hasReview: reviewMap.has(pr.pr_id),
      review: reviewMap.get(pr.pr_id),
    }))
  },
}
