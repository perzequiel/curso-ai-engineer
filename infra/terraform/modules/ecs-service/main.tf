terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

variable "name" { type = string }
variable "cluster_id" { type = string }
variable "cluster_name" { type = string }
variable "execution_role_arn" { type = string }
variable "task_role_arn" { type = string }
variable "image" { type = string }
variable "container_port" { type = number }
variable "subnet_ids" { type = list(string) }
variable "security_group_ids" { type = list(string) }

variable "cpu" {
  type    = string
  default = "256"
}

variable "memory" {
  type    = string
  default = "512"
}

variable "desired_count" {
  type    = number
  default = 1
}

variable "assign_public_ip" {
  type    = bool
  default = true
}

variable "target_group_arn" {
  type    = string
  default = null
}

variable "environment" {
  type    = map(string)
  default = {}
}

variable "secrets" {
  type    = map(string)
  default = {}
}

variable "health_check_command" {
  type    = list(string)
  default = []
}

variable "log_retention_days" {
  type    = number
  default = 7
}

variable "register_with_lb" {
  type    = bool
  default = true
}

variable "enable_autoscaling" {
  type    = bool
  default = false
}

variable "min_capacity" {
  type    = number
  default = 1
}

variable "max_capacity" {
  type    = number
  default = 2
}

variable "service_discovery_namespace_id" {
  type    = string
  default = null
}

variable "service_discovery_name" {
  type    = string
  default = null
}

variable "efs_volume" {
  type = object({
    efs_id          = string
    access_point_id = string
    mount_path      = string
    volume_name     = optional(string, "data")
  })
  default = null
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/ecs/${var.name}"
  retention_in_days = var.log_retention_days
}

data "aws_region" "current" {}

locals {
  volume_name = var.efs_volume != null ? coalesce(try(var.efs_volume.volume_name, null), "data") : null

  mount_points = var.efs_volume != null ? [{
    sourceVolume  = local.volume_name
    containerPath = var.efs_volume.mount_path
    readOnly      = false
  }] : []

  container = merge({
    name         = var.name
    image        = var.image
    essential    = true
    portMappings = [{ containerPort = var.container_port, protocol = "tcp" }]
    environment  = [for k, v in var.environment : { name = k, value = v }]
    secrets      = [for k, v in var.secrets : { name = k, valueFrom = v }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.this.name
        awslogs-region        = data.aws_region.current.name
        awslogs-stream-prefix = var.name
      }
    }
    }, length(local.mount_points) > 0 ? { mountPoints = local.mount_points } : {}, length(var.health_check_command) > 0 ? {
    healthCheck = {
      command     = var.health_check_command
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  } : {})
}

resource "aws_ecs_task_definition" "this" {
  family                   = var.name
  cpu                      = var.cpu
  memory                   = var.memory
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  execution_role_arn       = var.execution_role_arn
  task_role_arn            = var.task_role_arn
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }

  dynamic "volume" {
    for_each = var.efs_volume != null ? [var.efs_volume] : []
    content {
      name = local.volume_name
      efs_volume_configuration {
        file_system_id     = volume.value.efs_id
        transit_encryption = "ENABLED"
        authorization_config {
          access_point_id = volume.value.access_point_id
          iam             = "ENABLED"
        }
      }
    }
  }

  container_definitions = jsonencode([local.container])
}

resource "aws_service_discovery_service" "this" {
  count = var.service_discovery_name != null ? 1 : 0
  name  = var.service_discovery_name

  dns_config {
    namespace_id = var.service_discovery_namespace_id
    dns_records {
      ttl  = 10
      type = "A"
    }
    routing_policy = "MULTIVALUE"
  }

  health_check_custom_config {
    failure_threshold = 1
  }
}

resource "aws_ecs_service" "this" {
  name            = var.name
  cluster         = var.cluster_id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = var.desired_count
  launch_type     = "FARGATE"

  deployment_minimum_healthy_percent = 100
  deployment_maximum_percent         = 200

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  network_configuration {
    subnets          = var.subnet_ids
    security_groups  = var.security_group_ids
    assign_public_ip = var.assign_public_ip
  }

  dynamic "load_balancer" {
    for_each = var.register_with_lb && var.target_group_arn != null ? [1] : []
    content {
      target_group_arn = var.target_group_arn
      container_name   = var.name
      container_port   = var.container_port
    }
  }

  dynamic "service_registries" {
    for_each = length(aws_service_discovery_service.this) > 0 ? [1] : []
    content {
      registry_arn = aws_service_discovery_service.this[0].arn
    }
  }

  health_check_grace_period_seconds = var.register_with_lb ? 120 : null
  propagate_tags                    = "SERVICE"

  # task_definition NO se ignora: terraform es source of truth y pinea la ultima revision.
  # desired_count si, para no pisar autoscaling.
  lifecycle { ignore_changes = [desired_count] }

  depends_on = [aws_service_discovery_service.this]
}

resource "aws_appautoscaling_target" "this" {
  count              = var.enable_autoscaling ? 1 : 0
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${var.cluster_name}/${aws_ecs_service.this.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  count              = var.enable_autoscaling ? 1 : 0
  name               = "${var.name}-cpu-60"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.this[0].resource_id
  scalable_dimension = aws_appautoscaling_target.this[0].scalable_dimension
  service_namespace  = aws_appautoscaling_target.this[0].service_namespace
  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 60
    scale_in_cooldown  = 60
    scale_out_cooldown = 60
  }
}

output "service_name" { value = aws_ecs_service.this.name }
output "task_definition" { value = aws_ecs_task_definition.this.arn }
output "log_group" { value = aws_cloudwatch_log_group.this.name }
output "discovery_dns" {
  value = var.service_discovery_namespace_id != null && var.service_discovery_name != null ? "${var.service_discovery_name}.${var.cluster_name}.local" : null
}
