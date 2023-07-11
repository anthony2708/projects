# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Create a DB instance
resource "aws_db_instance" "example" {
  engine              = "mysql"
  allocated_storage   = 10
  instance_class      = "db.t2.micro"
  db_name             = "anthony_terraform"
  username            = "admin"
  password            = var.db_password
  skip_final_snapshot = true
  # TODO: Create 2 subnets in the same group 
  # db_subnet_group_name = 
}
