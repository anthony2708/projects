data "aws_availability_zones" "available" {}
data "aws_partition" "current" {}

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "region" {
  description = "The region of the EKS Cluster (need for migrating to different regions)"
  default     = "us-west-2"
}

variable "cidr" {
  description = "The network of the cluster"
  default     = "10.0.0.0/16"
}

variable "bucket_name" {
  description = "The name of the S3 backend bucket"
  default     = "anthony_terraform_bucket"
}

variable "db_table" {
  description = "The name of the AWS DynamoDB table"
  default     = "anthony_terraform_state"
}
variable "cluster_name" {
  description = "The name of the EKS Cluster"
  default     = "HelmTestCluster"
}

variable "cluster_version" {
  description = "The version of the EKS Cluster (need for upgrading)"
  default     = "1.22"
}

variable "karpenter_version" {
  description = "The version of the Scheduler"
  default     = "v0.16.3"
}

variable "namespace" {
  description = "The namespace of the application"
  default     = "karpenter"
}

locals {
  partition = data.aws_partition.current.partition
}