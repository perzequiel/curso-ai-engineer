import type { PRSummaryResponse, ReviewResponse } from "./types"

export const mockPRs: PRSummaryResponse[] = [
  {
    pr_id: "101",
    title: "feat: Add user authentication module",
    description: "Implements JWT-based authentication with refresh tokens",
    author: "john.doe",
    state: "open",
    url: "https://github.com/org/repo/pull/101",
  },
  {
    pr_id: "102",
    title: "fix: Resolve memory leak in WebSocket handler",
    description: "Fixes the memory leak issue reported in #98",
    author: "jane.smith",
    state: "open",
    url: "https://github.com/org/repo/pull/102",
  },
  {
    pr_id: "103",
    title: "refactor: Optimize database queries",
    description: "Reduces query time by 40% using proper indexing",
    author: "bob.wilson",
    state: "closed",
    url: "https://github.com/org/repo/pull/103",
  },
  {
    pr_id: "104",
    title: "docs: Update API documentation",
    description: "Adds missing endpoint documentation and examples",
    author: "alice.johnson",
    state: "open",
    url: "https://github.com/org/repo/pull/104",
  },
  {
    pr_id: "105",
    title: "feat: Implement dark mode support",
    description: "Adds theme switching capability with system preference detection",
    author: "charlie.brown",
    state: "merged",
    url: "https://github.com/org/repo/pull/105",
  },
  {
    pr_id: "106",
    title: "test: Add unit tests for payment module",
    description: "Increases test coverage to 85%",
    author: "diana.prince",
    state: "open",
    url: "https://github.com/org/repo/pull/106",
  },
  {
    pr_id: "107",
    title: "chore: Update dependencies",
    description: "Bumps all dependencies to latest stable versions",
    author: "evan.rogers",
    state: "closed",
    url: "https://github.com/org/repo/pull/107",
  },
]

export const mockReviews: ReviewResponse[] = [
  {
    id: "rev-001",
    pr_id: "101",
    status: "completed",
    rating: 8,
    summary: "Good implementation of authentication. Some minor security improvements suggested.",
    recommendations: [
      "Consider adding rate limiting to prevent brute force attacks",
      "Add token rotation mechanism",
      "Implement proper error handling for expired tokens",
    ],
    approved: true,
  },
  {
    id: "rev-002",
    pr_id: "103",
    status: "completed",
    rating: 9,
    summary: "Excellent optimization work. Significant performance improvements.",
    recommendations: [
      "Add query execution time logging for monitoring",
      "Consider adding database connection pooling",
    ],
    approved: true,
  },
  {
    id: "rev-003",
    pr_id: "105",
    status: "completed",
    rating: 7,
    summary: "Dark mode implementation is functional but needs some accessibility improvements.",
    recommendations: [
      "Ensure sufficient contrast ratios in dark mode",
      "Add prefers-reduced-motion support",
      "Test with screen readers",
    ],
    approved: false,
  },
]
