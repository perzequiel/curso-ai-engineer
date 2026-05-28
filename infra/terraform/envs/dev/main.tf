locals {
  name = "cursoai-${var.env}"
}

module "vpc" {
  source = "../../modules/vpc"
  name   = local.name
}

module "ecr" {
  source = "../../modules/ecr"
  name   = local.name
}

# Rol IAM asumido por GitHub Actions via OIDC para deploys (push ECR + update ECS).
# El ARN se setea como secret AWS_DEPLOY_ROLE_ARN en el repo.
module "iam_github_oidc" {
  source          = "../../modules/iam-github-oidc"
  name            = local.name
  github_repo     = var.github_repo
  github_branches = var.github_deploy_branches

  # El provider OIDC de GitHub ya existe en la cuenta (otra IaC lo creo).
  create_oidc_provider = false

  ecr_repository_arns = module.ecr.repository_arns
  pass_role_arns = [
    module.ecs_cluster.execution_role_arn,
    module.ecs_cluster.task_role_arn,
  ]
}

module "alb" {
  source            = "../../modules/alb"
  name              = local.name
  vpc_id            = module.vpc.vpc_id
  subnet_ids        = module.vpc.public_subnet_ids
  security_group_id = module.vpc.alb_sg_id
}

module "efs" {
  source             = "../../modules/efs"
  name               = local.name
  subnet_ids         = module.vpc.public_subnet_ids
  security_group_ids = [module.vpc.efs_sg_id]
}

resource "aws_secretsmanager_secret" "anthropic" {
  name = "${local.name}/anthropic_api_key"
}

resource "aws_secretsmanager_secret" "github" {
  name = "${local.name}/github_token"
}

resource "aws_secretsmanager_secret" "postgres_password" {
  name = "${local.name}/postgres_password"
}

resource "aws_secretsmanager_secret_version" "postgres_password" {
  secret_id     = aws_secretsmanager_secret.postgres_password.id
  secret_string = "changethis-after-apply"

  lifecycle {
    ignore_changes = [secret_string]
  }
}

module "ecs_cluster" {
  source = "../../modules/ecs-cluster"
  name   = local.name
  vpc_id = module.vpc.vpc_id

  secret_arns_read = [
    aws_secretsmanager_secret.anthropic.arn,
    aws_secretsmanager_secret.github.arn,
    aws_secretsmanager_secret.postgres_password.arn,
  ]

  efs_file_system_arns = [module.efs.arn]
}

module "svc_db" {
  source             = "../../modules/ecs-service"
  name               = "${local.name}-db"
  cluster_id         = module.ecs_cluster.cluster_id
  cluster_name       = module.ecs_cluster.cluster_name
  execution_role_arn = module.ecs_cluster.execution_role_arn
  task_role_arn      = module.ecs_cluster.task_role_arn
  image              = "pgvector/pgvector:pg16"
  container_port     = 5432
  cpu                = "512"
  memory             = "1024"
  subnet_ids         = module.vpc.public_subnet_ids
  security_group_ids = [module.vpc.db_sg_id, module.vpc.efs_sg_id]
  assign_public_ip   = true
  register_with_lb   = false

  service_discovery_namespace_id = module.ecs_cluster.service_discovery_namespace_id
  service_discovery_name         = "db"

  environment = {
    POSTGRES_DB   = "curso_ai"
    POSTGRES_USER = "app"
    PGDATA        = "/var/lib/postgresql/data/pgdata"
  }

  secrets = {
    POSTGRES_PASSWORD = aws_secretsmanager_secret.postgres_password.arn
  }

  efs_volume = {
    efs_id          = module.efs.id
    access_point_id = module.efs.access_point_id
    mount_path      = "/var/lib/postgresql/data"
    volume_name     = "postgres-data"
  }

  health_check_command = ["CMD-SHELL", "pg_isready -U app -d curso_ai || exit 1"]
}

module "svc_backend" {
  source             = "../../modules/ecs-service"
  name               = "${local.name}-backend"
  cluster_id         = module.ecs_cluster.cluster_id
  cluster_name       = module.ecs_cluster.cluster_name
  execution_role_arn = module.ecs_cluster.execution_role_arn
  task_role_arn      = module.ecs_cluster.task_role_arn
  image              = "${module.ecr.repository_urls["backend"]}:${var.image_tag}"
  container_port     = 8000
  cpu                = "512"
  memory             = "1024"
  subnet_ids         = module.vpc.public_subnet_ids
  security_group_ids = [module.vpc.backend_sg_id]
  assign_public_ip   = true
  target_group_arn   = module.alb.backend_tg_arn

  service_discovery_namespace_id = module.ecs_cluster.service_discovery_namespace_id
  service_discovery_name         = "backend"

  environment = {
    REPOSITORY_BACKEND = "db"
    POSTGRES_HOST      = "db.${module.ecs_cluster.service_discovery_namespace_name}"
    POSTGRES_PORT      = "5432"
    POSTGRES_USER      = "app"
    POSTGRES_DB        = "curso_ai"
    CORS_ORIGINS       = "http://${module.alb.dns_name}"
    GITHUB_REPO        = var.github_repo
  }

  secrets = {
    POSTGRES_PASSWORD = aws_secretsmanager_secret.postgres_password.arn
    ANTHROPIC_API_KEY = aws_secretsmanager_secret.anthropic.arn
    GITHUB_TOKEN      = aws_secretsmanager_secret.github.arn
  }

  depends_on = [module.svc_db]
}

module "svc_frontend" {
  source             = "../../modules/ecs-service"
  name               = "${local.name}-frontend"
  cluster_id         = module.ecs_cluster.cluster_id
  cluster_name       = module.ecs_cluster.cluster_name
  execution_role_arn = module.ecs_cluster.execution_role_arn
  task_role_arn      = module.ecs_cluster.task_role_arn
  image              = "${module.ecr.repository_urls["frontend"]}:${var.image_tag}"
  container_port     = 3000
  cpu                = "256"
  memory             = "512"
  subnet_ids         = module.vpc.public_subnet_ids
  security_group_ids = [module.vpc.frontend_sg_id]
  assign_public_ip   = true
  target_group_arn   = module.alb.frontend_tg_arn

  environment = {
    NEXT_PUBLIC_API_URL = "http://${module.alb.dns_name}"
  }

  depends_on = [module.svc_backend]
}
