#!/bin/bash
set -e

AWS_ACCESS_KEY_ID=$1
AWS_SECRET_ACCESS_KEY=$2

# Export AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY
if [ ! -n "$1" ] && [ ! -n "$2" ]; then
    echo "You did not provide enough credentials for AWS"
    exit 1
fi
echo "Exporting the key..."

# Create main Terraform file
mkdir ~/code/terraform/learn-terraform-aws-instance
cd ~/code/terraform/learn-terraform-aws-instance
touch main.tf
cat <<EoF > main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-west-2"
}

resource "aws_instance" "app_server" {
  ami           = "ami-830c94e3"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}
EoF

# Run the program & Check for errors
terraform init
terraform fmt # Format the code
terraform validate # Validate the code
terraform plan # Check for errors
terraform apply 
terraform show
terraform state list
terraform destroy

# Setup variables and change some values
touch variables.tf
cat <<EoF > variables.tf
variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "ExampleAppServerInstance"
}
EoF

terraform apply
terraform apply -var "instance_name=NewTeraEC2"

# Setup outputs and change some values
touch outputs.tf
cat <<EoF > outputs.tf
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}
EoF

terraform apply
terraform output
terraform destroy
