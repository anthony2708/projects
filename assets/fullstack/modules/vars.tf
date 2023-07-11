# Input variable: server port
variable "server_port" {
  description = "The port the server will use for HTTP requests"
  default     = "8080"
}

# Input variable: Cluster name
variable "cluster_name" {
  description = "The name to use for all the cluster resources"
}

# Input variable: DB remote state bucket name
variable "db_remote_state_bucket" {
  description = "The name of the S3 bucket for the database's remote state"
}

# Input variable: DB remote state bucket key
variable "db_remote_state_key" {
  description = "The path for database's remote state in S3"
}

variable "db_password" {
  description = "The password for the database"
  sensitive   = true
}

variable "db_host" {
  description = "The host endpoint for the database"
}

variable "db_name" {
  description = "The name for the database"
}

# Input variable: Instance type
variable "instance_type" {
  description = "The type of EC2 Instances to run (e.g. t2.micro)"
}

variable "environment" {
  description = "Environment used for the deployment"
}

# Input variable: AMI
variable "ami" {
  description = "The AMI to run in the cluster"
  default     = "ami-830c94e3"
}

# Input variable
variable "min_size" {}

variable "max_size" {}

variable "web_version" {
  description = "The version of the application"
}