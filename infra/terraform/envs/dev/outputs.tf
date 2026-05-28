output "alb_url" {
  description = "URL HTTP de la aplicacion (ALB)"
  value       = "http://${module.alb.dns_name}"
}

output "github_deploy_role_arn" {
  description = "ARN del rol IAM para GitHub Actions. Setearlo como secret AWS_DEPLOY_ROLE_ARN."
  value       = module.iam_github_oidc.role_arn
}

output "alb_dns_name" {
  value = module.alb.dns_name
}

output "cluster_name" {
  value = module.ecs_cluster.cluster_name
}

output "ecr_repository_urls" {
  value = module.ecr.repository_urls
}

output "postgres_host" {
  description = "Hostname interno de Postgres (Cloud Map)"
  value       = "db.${module.ecs_cluster.service_discovery_namespace_name}"
}

output "service_names" {
  value = {
    backend  = module.svc_backend.service_name
    frontend = module.svc_frontend.service_name
    db       = module.svc_db.service_name
  }
}
