variable "name" {
  type        = string
  description = "Prefijo de nombres para el rol y policy (ej: cursoai-dev)."
}

variable "github_repo" {
  type        = string
  description = "Repositorio GitHub en formato owner/repo (ej: perzequiel/curso-ai-engineer)."
}

variable "github_branches" {
  type        = list(string)
  description = "Branches del repo autorizados a asumir el rol via OIDC."
  default     = ["main-api"]
}

variable "create_oidc_provider" {
  type        = bool
  description = "Crear el OIDC provider. Poner false si ya existe en la cuenta."
  default     = true
}

variable "ecr_repository_arns" {
  type        = list(string)
  description = "ARNs de los repos ECR a los que se permite push."
}

variable "pass_role_arns" {
  type        = list(string)
  description = "Roles IAM (task / execution) que el deploy puede pasar al registrar task definitions."
}
