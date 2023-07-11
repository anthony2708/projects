provider "aws" {
  region = "us-west-2"
}

module "cluster" {
  source = "../../../modules"

  ami = "ami-830c94e3"

  cluster_name           = "web-prod"
  db_remote_state_bucket = var.db_remote_state_bucket
  db_remote_state_key    = var.db_remote_state_key
  db_host                = var.db_host
  db_password            = var.db_password
  db_name                = var.db_name

  environment   = var.environment
  instance_type = "t2.micro"
  min_size      = 1
  max_size      = 5
  web_version   = var.web_version
}

