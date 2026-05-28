terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

variable "name" { type = string }
variable "vpc_id" { type = string }

variable "secret_arns_read" {
  type    = list(string)
  default = []
}

variable "efs_file_system_arns" {
  type    = list(string)
  default = []
}

resource "aws_ecs_cluster" "this" {
  name = var.name
  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_service_discovery_private_dns_namespace" "this" {
  name        = "${var.name}.local"
  description = "Service discovery for ${var.name}"
  vpc         = var.vpc_id
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "exec" {
  name               = "${var.name}-task-exec"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy_attachment" "exec_managed" {
  role       = aws_iam_role.exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "exec_secrets" {
  count = length(var.secret_arns_read) > 0 ? 1 : 0
  name  = "secrets-read"
  role  = aws_iam_role.exec.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = var.secret_arns_read
    }]
  })
}

resource "aws_iam_role" "task" {
  name               = "${var.name}-task-app"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

resource "aws_iam_role_policy" "task_logs" {
  name = "app-runtime"
  role = aws_iam_role.task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["logs:CreateLogStream", "logs:PutLogEvents"]
      Resource = "*"
    }]
  })
}

resource "aws_iam_role_policy" "task_efs" {
  count = length(var.efs_file_system_arns) > 0 ? 1 : 0
  name  = "efs-mount"
  role  = aws_iam_role.task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "elasticfilesystem:ClientMount",
        "elasticfilesystem:ClientWrite",
        "elasticfilesystem:ClientRootAccess",
      ]
      Resource = var.efs_file_system_arns
    }]
  })
}

output "cluster_id" { value = aws_ecs_cluster.this.id }
output "cluster_name" { value = aws_ecs_cluster.this.name }
output "execution_role_arn" { value = aws_iam_role.exec.arn }
output "task_role_arn" { value = aws_iam_role.task.arn }
output "service_discovery_namespace_id" { value = aws_service_discovery_private_dns_namespace.this.id }
output "service_discovery_namespace_name" { value = aws_service_discovery_private_dns_namespace.this.name }
