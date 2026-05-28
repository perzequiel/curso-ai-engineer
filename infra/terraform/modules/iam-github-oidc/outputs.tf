output "role_arn" {
  description = "ARN del rol asumible por GitHub Actions. Setear como secret AWS_DEPLOY_ROLE_ARN."
  value       = aws_iam_role.deploy.arn
}

output "role_name" {
  value = aws_iam_role.deploy.name
}

output "oidc_provider_arn" {
  value = local.oidc_provider_arn
}
