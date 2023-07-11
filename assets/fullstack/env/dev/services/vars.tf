variable "db_remote_state_bucket" {
  default = "anthony-terraform-bucket"
}

variable "db_remote_state_key" {
  default = "env/dev/mysql/terraform.tfstate"
}

variable "db_host" {
  description = "The endpoint for the RDS Database"
}

variable "db_password" {
  description = "The password for the RDS Database"
  sensitive   = true
}

variable "environment" {
  default = "dev"
}

variable "web_version" {
}

variable "db_name" {
  default = "anthony_terraform_stage"
}