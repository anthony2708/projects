# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Create an EC2 instance
resource "aws_instance" "example" {
  ami           = "ami-830c94e3"
  instance_type = "t2.micro"
}
