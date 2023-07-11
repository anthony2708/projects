# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Data source: query the list of availability zones
# data "aws_availability_zones" "all" {}

# Data source: DB remote state
data "terraform_remote_state" "db" {
  backend = "s3"
  
  config {
    bucket = "${var.db_remote_state_bucket}"
    key    = "${var.db_remote_state_key}"
    region = "us-west-2"
  }
}

# Data source: Template file
data "template_file" "user_data" {
  template = "${file("user-data.sh")}"
  
  vars {
    server_port = "${var.server_port}"
    db_address  = "${data.terraform_remote_state.db.address}"
    db_port     = "${data.terraform_remote_state.db.port}"
  }
}

# Create a Security Group for an EC2 instance
resource "aws_security_group" "instance" {
  name = "terraform-example-instance"
  
  ingress {
    from_port	  = "${var.server_port}"
    to_port		  = "${var.server_port}"
    protocol	  = "tcp"
    cidr_blocks	= ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# Create a Security Group for an ELB
resource "aws_security_group" "elb" {
  name = "terraform-example-elb"
  
  ingress {
    from_port	  = 80
    to_port	    = 80
    protocol	  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port	  = 0
    to_port	    = 0
    protocol	  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a Launch Configuration
resource "aws_launch_configuration" "example" {
  image_id	      = "ami-785db401"
  instance_type   = "t2.micro"
  security_groups = ["${aws_security_group.instance.id}"]
  user_data       = "${data.template_file.user_data.rendered}"
  
  lifecycle {
    create_before_destroy = true
  }
}

# Create an Autoscaling Group
resource "aws_autoscaling_group" "example" {
  launch_configuration = "${aws_launch_configuration.example.id}"
  availability_zones   = ["${data.aws_availability_zones.all.names}"]
  
  load_balancers       = ["${aws_elb.example.name}"]
  health_check_type    = "ELB"
  
  min_size = 1
  max_size = 5
  
  tag {
    key                 = "Name"
    value               = "terraform-asg-example"
    propagate_at_launch = true
  }
}

# Create an ELB
resource "aws_elb" "example" {
  name               = "terraform-asg-example"
  availability_zones = ["${data.aws_availability_zones.all.names}"]
  security_groups    = ["${aws_security_group.elb.id}"]
  
  listener {
    lb_port           = 80
    lb_protocol       = "http"
    instance_port     = "${var.server_port}"
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
