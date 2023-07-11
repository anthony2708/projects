output "cluster_id" {
  value       = module.eks.cluster_id
  description = "The ID of the EKS Cluster"
}

output "cluster_endpoint" {
  value       = module.eks.cluster_endpoint
  description = "The Endpoint of the EKS Cluster"
}

output "cluster_sg" {
  value       = module.eks.cluster_security_group_id
  description = "The Security Group of the Cluster"
}

output "cluster_name" {
  value       = var.cluster_name
  description = "The name of the EKS Cluster"
}

output "region" {
  value       = var.region
  description = "The region of the EKS Cluster"
}

