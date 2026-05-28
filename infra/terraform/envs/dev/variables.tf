variable "region" {
  type    = string
  default = "us-east-1"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag for backend and frontend ECR images"
  default     = "latest"
}

variable "github_repo" {
  type        = string
  description = "GitHub repository in owner/repo format"
  default     = ""
}
