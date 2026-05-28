# OIDC provider de GitHub Actions + rol IAM asumible por workflows del repo,
# restringido a un set explicito de branches.

locals {
  oidc_provider_url = "token.actions.githubusercontent.com"
  # Lista de "sub" claims permitidos: repo + branch.
  allowed_subs = [
    for b in var.github_branches : "repo:${var.github_repo}:ref:refs/heads/${b}"
  ]
}

# Crea el provider OIDC en la cuenta. Si ya existe (otra IaC, otro repo),
# poner create_oidc_provider=false y referenciar el existente via data.
resource "aws_iam_openid_connect_provider" "github" {
  count = var.create_oidc_provider ? 1 : 0

  url            = "https://${local.oidc_provider_url}"
  client_id_list = ["sts.amazonaws.com"]
  # Thumbprints publicados por GitHub (rotaron en 2023; se aceptan ambos).
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd",
  ]
}

data "aws_iam_openid_connect_provider" "existing" {
  count = var.create_oidc_provider ? 0 : 1
  url   = "https://${local.oidc_provider_url}"
}

locals {
  oidc_provider_arn = var.create_oidc_provider ? aws_iam_openid_connect_provider.github[0].arn : data.aws_iam_openid_connect_provider.existing[0].arn
}

data "aws_iam_policy_document" "assume" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [local.oidc_provider_arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.oidc_provider_url}:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Restringe el rol a los branches especificados.
    condition {
      test     = "StringEquals"
      variable = "${local.oidc_provider_url}:sub"
      values   = local.allowed_subs
    }
  }
}

resource "aws_iam_role" "deploy" {
  name               = "${var.name}-gha-deploy"
  description        = "Rol asumido por GitHub Actions (OIDC) para deploys de ${var.github_repo}"
  assume_role_policy = data.aws_iam_policy_document.assume.json
}

data "aws_iam_policy_document" "deploy" {
  # ECR: token de autenticacion (global, no scoped por arn).
  statement {
    sid       = "EcrAuth"
    actions   = ["ecr:GetAuthorizationToken"]
    resources = ["*"]
  }

  # ECR: push/pull a los repos del proyecto.
  statement {
    sid = "EcrPush"
    actions = [
      "ecr:BatchCheckLayerAvailability",
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:InitiateLayerUpload",
      "ecr:UploadLayerPart",
      "ecr:CompleteLayerUpload",
      "ecr:PutImage",
      "ecr:DescribeRepositories",
      "ecr:DescribeImages",
    ]
    resources = var.ecr_repository_arns
  }

  # ECS: registrar task defs, actualizar servicios, esperar rollout.
  statement {
    sid = "EcsDeploy"
    actions = [
      "ecs:RegisterTaskDefinition",
      "ecs:DescribeTaskDefinition",
      "ecs:UpdateService",
      "ecs:DescribeServices",
      "ecs:ListServices",
      "ecs:ListTasks",
      "ecs:DescribeTasks",
    ]
    resources = ["*"]
  }

  # Necesario para registrar task definitions que referencian task/execution roles.
  statement {
    sid       = "PassEcsRoles"
    actions   = ["iam:PassRole"]
    resources = var.pass_role_arns
    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"
      values   = ["ecs-tasks.amazonaws.com"]
    }
  }

  # ALB lookup (deploy.yml usa describe-load-balancers para resolver el DNS).
  statement {
    sid       = "AlbDescribe"
    actions   = ["elbv2:DescribeLoadBalancers"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "deploy" {
  name   = "${var.name}-gha-deploy"
  policy = data.aws_iam_policy_document.deploy.json
}

resource "aws_iam_role_policy_attachment" "deploy" {
  role       = aws_iam_role.deploy.name
  policy_arn = aws_iam_policy.deploy.arn
}
