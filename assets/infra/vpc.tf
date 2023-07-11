# Create a new VPC for an EC2 instance
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
  instance_tenancy = "default"
  tags = {
    "Name" = "vpc-test"
  }
}

# Create EIP
resource "aws_eip" "eip" {
  vpc = true
}

# Create Internet Gateway 
resource "aws_internet_gateway" "tf_gateway" {
  vpc_id = aws_vpc.main.id
}

# Create NAT Gateway
resource "aws_nat_gateway" "natgw" {
  allocation_id = aws_eip.eip.id
  subnet_id     = aws_subnet.tf_subnet.id
}