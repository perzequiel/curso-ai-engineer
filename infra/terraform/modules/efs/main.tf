terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

variable "name" { type = string }
variable "subnet_ids" { type = list(string) }
variable "security_group_ids" { type = list(string) }

resource "aws_efs_file_system" "this" {
  encrypted = true
  tags      = { Name = "${var.name}-efs" }
}

resource "aws_efs_mount_target" "this" {
  count           = length(var.subnet_ids)
  file_system_id  = aws_efs_file_system.this.id
  subnet_id       = var.subnet_ids[count.index]
  security_groups = var.security_group_ids
}

resource "aws_efs_access_point" "postgres" {
  file_system_id = aws_efs_file_system.this.id

  posix_user {
    gid = 999
    uid = 999
  }

  root_directory {
    path = "/postgres"
    creation_info {
      owner_gid   = 999
      owner_uid   = 999
      permissions = "700"
    }
  }

  tags = { Name = "${var.name}-postgres-ap" }
}

output "id" { value = aws_efs_file_system.this.id }
output "arn" { value = aws_efs_file_system.this.arn }
output "access_point_id" { value = aws_efs_access_point.postgres.id }
