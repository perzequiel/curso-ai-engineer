"use client"

import { useState, useEffect, useCallback } from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Skeleton } from "@/components/ui/skeleton"
import { CheckCircle2, XCircle, Play, ExternalLink, GitPullRequest } from "lucide-react"
import { toast } from "sonner"
import { apiService, ApiError } from "@/lib/api-service"
import type { PRWithReviewStatus, PRState } from "@/lib/types"
import { ReviewDetailDialog } from "./review-detail-dialog"

function describeError(error: unknown, fallback: string): string {
  if (error instanceof ApiError) {
    return error.status === 0
      ? error.message
      : `${error.message} (HTTP ${error.status})`
  }
  if (error instanceof Error && error.message) {
    return error.message
  }
  return fallback
}

export function PRList() {
  const [prs, setPrs] = useState<PRWithReviewStatus[]>([])
  const [loading, setLoading] = useState(true)
  const [stateFilter, setStateFilter] = useState<PRState>("open")
  const [reviewFilter, setReviewFilter] = useState<"all" | "reviewed" | "pending">("all")
  const [creatingReview, setCreatingReview] = useState<string | null>(null)
  const [selectedPR, setSelectedPR] = useState<PRWithReviewStatus | null>(null)
  const [dialogOpen, setDialogOpen] = useState(false)

  const fetchPRs = useCallback(async () => {
    setLoading(true)
    try {
      const data = await apiService.getPRsWithReviewStatus(stateFilter)
      setPrs(data)
    } catch (error) {
      console.error("Error fetching PRs:", error)
      setPrs([])
      toast.error("No se pudo cargar la lista de PRs", {
        description: describeError(error, "Error desconocido al consultar la API"),
      })
    } finally {
      setLoading(false)
    }
  }, [stateFilter])

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    fetchPRs()
  }, [fetchPRs])

  const handleCreateReview = async (prId: string) => {
    setCreatingReview(prId)
    const inProgress = toast.loading(`Revisando PR #${prId}...`, {
      description: "Esto puede tardar unos segundos.",
    })
    try {
      const review = await apiService.createReview({ pr_id: prId })
      toast.success(`Review del PR #${prId} completada`, {
        id: inProgress,
        description: review.approved
          ? `Aprobado · Rating ${review.rating ?? "N/A"}/100`
          : `Cambios requeridos · Rating ${review.rating ?? "N/A"}/100`,
      })
      await fetchPRs()
    } catch (error) {
      console.error("Error creating review:", error)
      toast.error(`No se pudo revisar el PR #${prId}`, {
        id: inProgress,
        description: describeError(error, "Error desconocido al crear la review"),
      })
    } finally {
      setCreatingReview(null)
    }
  }

  const handleViewReview = (pr: PRWithReviewStatus) => {
    setSelectedPR(pr)
    setDialogOpen(true)
  }

  const filteredPRs = prs.filter((pr) => {
    if (reviewFilter === "reviewed") return pr.hasReview
    if (reviewFilter === "pending") return !pr.hasReview
    return true
  })

  const getStateBadgeVariant = (state: string) => {
    switch (state) {
      case "open":
        return "default"
      case "closed":
        return "secondary"
      case "merged":
        return "outline"
      default:
        return "default"
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2">
          <GitPullRequest className="h-6 w-6" />
          <h1 className="text-2xl font-bold">Pull Requests</h1>
        </div>
        <div className="flex flex-col gap-2 sm:flex-row">
          <Select
            value={stateFilter}
            onValueChange={(value: PRState) => setStateFilter(value)}
          >
            <SelectTrigger className="w-[140px]">
              <SelectValue placeholder="Estado" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="open">Abiertos</SelectItem>
              <SelectItem value="closed">Cerrados</SelectItem>
            </SelectContent>
          </Select>

          <Select
            value={reviewFilter}
            onValueChange={(value: "all" | "reviewed" | "pending") =>
              setReviewFilter(value)
            }
          >
            <SelectTrigger className="w-[160px]">
              <SelectValue placeholder="Review" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Todos</SelectItem>
              <SelectItem value="reviewed">Con Review</SelectItem>
              <SelectItem value="pending">Sin Review</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead className="w-[80px]">PR ID</TableHead>
              <TableHead className="w-1/2">Título</TableHead>
              <TableHead className="hidden md:table-cell w-[160px]">Autor</TableHead>
              <TableHead className="w-[100px]">Estado</TableHead>
              <TableHead className="w-[100px]">Review</TableHead>
              <TableHead className="w-[120px] text-right">Acciones</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {loading ? (
              Array.from({ length: 5 }).map((_, i) => (
                <TableRow key={i}>
                  <TableCell>
                    <Skeleton className="h-4 w-12" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-4 w-64" />
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    <Skeleton className="h-4 w-24" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-5 w-16" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-5 w-16" />
                  </TableCell>
                  <TableCell>
                    <Skeleton className="h-8 w-20 ml-auto" />
                  </TableCell>
                </TableRow>
              ))
            ) : filteredPRs.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="h-24 text-center">
                  No se encontraron Pull Requests
                </TableCell>
              </TableRow>
            ) : (
              filteredPRs.map((pr) => (
                <TableRow key={pr.pr_id} className="align-top">
                  <TableCell className="font-mono text-sm">
                    #{pr.pr_id}
                  </TableCell>
                  <TableCell className="max-w-0">
                    <div className="flex flex-col gap-1 min-w-0">
                      <span className="font-medium break-words">
                        {pr.title}
                      </span>
                      <span className="text-xs text-muted-foreground line-clamp-2 break-words hidden sm:block">
                        {pr.description}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="hidden md:table-cell">
                    <span className="text-sm text-muted-foreground">
                      @{pr.author}
                    </span>
                  </TableCell>
                  <TableCell>
                    <Badge variant={getStateBadgeVariant(pr.state)}>
                      {pr.state}
                    </Badge>
                  </TableCell>
                  <TableCell>
                    {pr.hasReview ? (
                      <Button
                        variant="ghost"
                        size="sm"
                        className="gap-1 text-green-600 hover:text-green-700 p-0"
                        onClick={() => handleViewReview(pr)}
                      >
                        <CheckCircle2 className="h-4 w-4" />
                        <span className="hidden sm:inline">Ver</span>
                      </Button>
                    ) : (
                      <div className="flex items-center gap-1 text-muted-foreground">
                        <XCircle className="h-4 w-4" />
                        <span className="text-xs hidden sm:inline">Pendiente</span>
                      </div>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    <div className="flex items-center justify-end gap-1">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleCreateReview(pr.pr_id)}
                        disabled={creatingReview === pr.pr_id}
                      >
                        {creatingReview === pr.pr_id ? (
                          <span className="flex items-center gap-1">
                            <span className="h-3 w-3 animate-spin rounded-full border-2 border-current border-t-transparent" />
                            <span className="hidden sm:inline">Revisando...</span>
                          </span>
                        ) : (
                          <span className="flex items-center gap-1">
                            <Play className="h-3 w-3" />
                            <span>PR</span>
                          </span>
                        )}
                      </Button>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8"
                        onClick={() => window.open(pr.url, "_blank")}
                      >
                        <ExternalLink className="h-4 w-4" />
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>

      <ReviewDetailDialog
        pr={selectedPR}
        open={dialogOpen}
        onOpenChange={setDialogOpen}
      />
    </div>
  )
}
