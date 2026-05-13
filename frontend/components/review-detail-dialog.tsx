"use client"

import { useState, useEffect } from "react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { CheckCircle2, XCircle, AlertCircle, ListChecks } from "lucide-react"
import { apiService } from "@/lib/api-service"
import type { PRWithReviewStatus, ReviewResponse } from "@/lib/types"

interface ReviewDetailDialogProps {
  pr: PRWithReviewStatus | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function ReviewDetailDialog({
  pr,
  open,
  onOpenChange,
}: ReviewDetailDialogProps) {
  const [review, setReview] = useState<ReviewResponse | null>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!open || !pr?.pr_id) {
      return
    }
    let cancelled = false
    setLoading(true)
    setReview(null)
    apiService
      .getReview(pr.pr_id)
      .then((data) => {
        if (!cancelled) setReview(data)
      })
      .catch((error) => {
        console.error("Error fetching review:", error)
        if (!cancelled) setReview(null)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [open, pr?.pr_id])

  // Rating is on a 0-100 scale (approval threshold = 70 in the backend).
  const getRatingColor = (rating: number | null) => {
    if (rating === null) return "bg-muted"
    if (rating >= 80) return "bg-green-500"
    if (rating >= 60) return "bg-yellow-500"
    return "bg-red-500"
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "completed":
        return <CheckCircle2 className="h-4 w-4 text-green-600" />
      case "in_progress":
        return <AlertCircle className="h-4 w-4 text-yellow-600" />
      default:
        return <AlertCircle className="h-4 w-4 text-muted-foreground" />
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <span>Review del PR #{pr?.pr_id}</span>
            {review?.approved !== undefined && (
              <Badge variant={review.approved ? "default" : "destructive"}>
                {review.approved ? "Aprobado" : "Cambios Requeridos"}
              </Badge>
            )}
          </DialogTitle>
          <DialogDescription>{pr?.title}</DialogDescription>
        </DialogHeader>

        {loading ? (
          <div className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-20 w-full" />
          </div>
        ) : review ? (
          <div className="space-y-6">
            {/* Status and Rating */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <span className="text-sm font-medium text-muted-foreground">
                  Estado
                </span>
                <div className="flex items-center gap-2">
                  {getStatusIcon(review.status)}
                  <span className="capitalize">{review.status}</span>
                </div>
              </div>
              <div className="space-y-2">
                <span className="text-sm font-medium text-muted-foreground">
                  Rating
                </span>
                <div className="flex items-center gap-2">
                  <Progress
                    value={review.rating ?? 0}
                    className="h-2 flex-1"
                  />
                  <span
                    className={`text-sm font-bold px-2 py-0.5 rounded ${getRatingColor(review.rating)} text-white`}
                  >
                    {review.rating ?? "N/A"}/100
                  </span>
                </div>
              </div>
            </div>

            <Separator />

            {/* Summary */}
            <div className="space-y-2">
              <span className="text-sm font-medium">Resumen</span>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {review.summary}
              </p>
            </div>

            <Separator />

            {/* Recommendations */}
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <ListChecks className="h-4 w-4" />
                <span className="text-sm font-medium">Recomendaciones</span>
              </div>
              {review.recommendations.length > 0 ? (
                <ul className="space-y-2">
                  {review.recommendations.map((rec, index) => (
                    <li
                      key={index}
                      className="flex items-start gap-2 text-sm text-muted-foreground"
                    >
                      <span className="text-primary mt-1">•</span>
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-muted-foreground">
                  No hay recomendaciones adicionales.
                </p>
              )}
            </div>

            {/* Approval Status */}
            <div className="flex items-center gap-2 p-4 rounded-lg bg-muted/50">
              {review.approved ? (
                <>
                  <CheckCircle2 className="h-5 w-5 text-green-600" />
                  <span className="text-sm font-medium">
                    Este PR ha sido aprobado para merge
                  </span>
                </>
              ) : (
                <>
                  <XCircle className="h-5 w-5 text-red-500" />
                  <span className="text-sm font-medium">
                    Se requieren cambios antes de hacer merge
                  </span>
                </>
              )}
            </div>
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <XCircle className="h-12 w-12 text-muted-foreground mb-4" />
            <p className="text-muted-foreground">
              No se encontró información del review para este PR.
            </p>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
