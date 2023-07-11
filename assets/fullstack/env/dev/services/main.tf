provider "aws" {
  region = "us-west-2"
}

module "cluster" {
  source = "../../../modules"

  ami = "ami-830c94e3"

  cluster_name           = "web-dev"
  db_remote_state_bucket = var.db_remote_state_bucket
  db_remote_state_key    = var.db_remote_state_key
  db_host                = var.db_host
  db_password            = var.db_password
  db_name                = var.db_name

  environment   = var.environment
  instance_type = "t2.micro"
  max_size      = 2
  min_size      = 1
  web_version   = var.web_version
}

# resource "aws_security_group_rule" "allow_test_inbound" {
#   type              = "ingress"
#   security_group_id = module.ecs.elb_sg_id

#   from_port   = 12345
#   to_port     = 12345
#   protocol    = "tcp"
#   cidr_blocks = ["0.0.0.0/0"]
# }