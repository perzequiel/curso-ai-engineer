terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.60" }
  }
}

variable "name" { type = string }
variable "vpc_id" { type = string }
variable "subnet_ids" { type = list(string) }
variable "security_group_id" { type = string }

resource "aws_lb" "this" {
  name               = "${var.name}-alb"
  load_balancer_type = "application"
  subnets            = var.subnet_ids
  security_groups    = [var.security_group_id]
  ip_address_type    = "ipv4"
}

resource "aws_lb_target_group" "backend" {
  name_prefix = "be-"
  vpc_id      = var.vpc_id
  port        = 8000
  protocol    = "HTTP"
  target_type = "ip"
  health_check {
    path                = "/docs"
    matcher             = "200-399"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
  deregistration_delay = 30
  lifecycle { create_before_destroy = true }
}

resource "aws_lb_target_group" "frontend" {
  name_prefix = "fe-"
  vpc_id      = var.vpc_id
  port        = 3000
  protocol    = "HTTP"
  target_type = "ip"
  health_check {
    path                = "/"
    matcher             = "200-399"
    interval            = 30
    healthy_threshold   = 2
    unhealthy_threshold = 3
  }
  deregistration_delay = 30
  lifecycle { create_before_destroy = true }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.frontend.arn
  }
}

resource "aws_lb_listener_rule" "backend" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 10
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
  condition {
    path_pattern {
      values = ["/reviews", "/reviews/*", "/prs", "/prs/*", "/docs"]
    }
  }
}

resource "aws_lb_listener_rule" "backend_extra" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 11
  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.backend.arn
  }
  condition {
    path_pattern {
      values = ["/docs/*", "/openapi.json", "/redoc", "/redoc/*"]
    }
  }
}

output "dns_name" { value = aws_lb.this.dns_name }
output "zone_id" { value = aws_lb.this.zone_id }
output "backend_tg_arn" { value = aws_lb_target_group.backend.arn }
output "frontend_tg_arn" { value = aws_lb_target_group.frontend.arn }
output "http_listener_arn" { value = aws_lb_listener.http.arn }
