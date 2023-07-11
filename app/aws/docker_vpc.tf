module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.2"

  name = "${var.app_name}-${terraform.workspace}-vpc"
  cidr = var.cidr
  azs  = slice(data.aws_availability_zones.available.names, 0, 3)

  private_subnets = [
    cidrsubnet(var.cidr, 8, 1),
    cidrsubnet(var.cidr, 8, 2),
    cidrsubnet(var.cidr, 8, 3)
  ]
  public_subnets = [
    cidrsubnet(var.cidr, 8, 4),
    cidrsubnet(var.cidr, 8, 5),
    cidrsubnet(var.cidr, 8, 6)
  ]

  enable_nat_gateway     = false
  single_nat_gateway     = false
  enable_dns_hostnames   = true
  one_nat_gateway_per_az = false
}

resource "aws_eip" "docker" {
  depends_on = [
    module.vpc,
    aws_instance.docker
  ]

  instance = aws_instance.docker.id
  vpc      = true
}

resource "aws_key_pair" "ec2_key" {
  key_name   = "ec2_key"
  public_key = file("./certs/ec2_key.pub")
}

resource "aws_instance" "docker" {
  depends_on = [
    aws_security_group.allow_docker,
    aws_key_pair.ec2_key,
    module.vpc
  ]

  ami                    = var.vm_ami
  instance_type          = "t2.micro"
  subnet_id              = module.vpc.public_subnets[0]
  vpc_security_group_ids = ["${aws_security_group.allow_docker.id}"]
  # user_data              = file("../scripts/docker.sh")
  # user_data_replace_on_change = true
  key_name               = aws_key_pair.ec2_key.key_name
  tags = {
    Name = "docker-${terraform.workspace}"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_security_group" "allow_docker" {
  name        = "allow_docker"
  description = "Allow docker access"
  vpc_id      = module.vpc.vpc_id
  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/32"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Allow Outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}