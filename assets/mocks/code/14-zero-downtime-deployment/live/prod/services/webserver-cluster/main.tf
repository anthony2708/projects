# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Use Module
module "webserver_cluster" {
  source = "../../../../modules/services/webserver-cluster"

  ami         = "ami-830c94e3"
  server_text = "Hello, World"

  cluster_name           = "werservers-prod"
  db_remote_state_bucket = var.db_remote_state_bucket
  db_remote_state_key    = var.db_remote_state_key

  instance_type      = "t2.micro"
  min_size           = 1
  max_size           = 5
  enable_autoscaling = true
}
