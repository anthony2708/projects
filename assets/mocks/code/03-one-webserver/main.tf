# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Create a Security Group for an EC2 instance
resource "aws_security_group" "instance" {
  name   = "terraform-example-instance"
  vpc_id = aws_vpc.main.id

  ingress {
    description = "VPC SG"
    from_port   = var.server_port
    to_port     = var.server_port
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create a security group for ELB
resource "aws_security_group" "elb" {
  name   = "terraform-example-elb"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an EC2 instance --> Launch Configuration
resource "aws_launch_configuration" "example" {
  # resource "aws_instance" "example" {
  # ami           = "ami-830c94e3"
  image_id      = "ami-830c94e3"
  instance_type = "t2.micro"
  # vpc_security_group_ids      = ["${aws_security_group.instance.id}"]
  security_groups = ["${aws_security_group.instance.id}"]
  # subnet_id                   = aws_subnet.tf_subnet.id
  # associate_public_ip_address = true

  user_data = <<-EOF
	      #!/bin/bash
	      echo "Hello, World" > index.html
	      nohup busybox httpd -f -p "${var.server_port}" &
	      EOF

  # tags = {
  #   Name = "terraform-example"
  # }
  lifecycle {
    create_before_destroy = true
  }
}

# Create an Autoscaling Group
resource "aws_autoscaling_group" "example" {
  launch_configuration = aws_launch_configuration.example.id
  vpc_zone_identifier = ["${aws_subnet.tf_subnet.id}"]

  load_balancers    = ["${aws_elb.example.name}"]
  health_check_type = "ELB"

  min_size = 1
  max_size = 5

  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

# Create a Load balancer
resource "aws_elb" "example" {
  name = "terraform-asg-example"
  security_groups = ["${aws_security_group.elb.id}"]
  subnets         = ["${aws_subnet.tf_subnet.id}"]

  listener {
    lb_port           = 80
    lb_protocol       = "http"
    instance_port     = var.server_port
    instance_protocol = "http"
  }

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    interval            = 30
    target              = "HTTP:${var.server_port}/"
  }
}