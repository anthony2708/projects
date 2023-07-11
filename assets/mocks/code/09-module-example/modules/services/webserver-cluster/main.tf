# Data source: query the list of availability zones
data "aws_availability_zones" "all" {}

# Data source: DB remote state
data "terraform_remote_state" "db" {
  backend = "s3"
  
  config {
	bucket = "${var.db_remote_state_bucket}"
	key    = "${var.db_remote_state_key}"
	region = "eu-west-1"
  }
}

# Data source: Template file
data "template_file" "user_data" {
  template = "${file("${path.module}/user-data.sh")}"
  
  vars {
    server_port = "${var.server_port}"
	db_address  = "${data.terraform_remote_state.db.address}"
	db_port     = "${data.terraform_remote_state.db.port}"
  }
}

# Create a Security Group for an EC2 instance
resource "aws_security_group" "instance" {
  name = "${var.cluster_name}-instance"
  
  lifecycle {
    create_before_destroy = true
  }
}

# Create a Security Group Rule
resource "aws_security_group_rule" "allow_server_http_inbound" {
  type = "ingress"
  security_group_id = "${aws_security_group.instance.id}"
  
  from_port	  = "${var.server_port}"
  to_port	  = "${var.server_port}"
  protocol	  = "tcp"
  cidr_blocks = ["0.0.0.0/0"]

}

# Create a Security Group for an ELB
resource "aws_security_group" "elb" {
  name = "${var.cluster_name}-elb"
}

# Create a Security Group Rule, inbound
resource "aws_security_group_rule" "allow_http_inbound" {
  type              = "ingress"
  security_group_id = "${aws_security_group.elb.id}"
  
  from_port	  = 80
  to_port	  = 80
  protocol	  = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Create a Security Group Rule, outbound
resource "aws_security_group_rule" "allow_all_outbound" {
  type              = "egress"
  security_group_id = "${aws_security_group.elb.id}"
  
  from_port	  = 0
  to_port	  = 0
  protocol	  = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

# Create a Launch Configuration
resource "aws_launch_configuration" "example" {
  image_id		  = "ami-785db401"
  instance_type   = "${var.instance_type}"
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
  
  min_size = "${var.min_size}"
  max_size = "${var.max_size}"
  
  tag {
    key                 = "Name"
    value               = "${var.cluster_name}"
    propagate_at_launch = true
  }
}

# Create an ELB
resource "aws_elb" "example" {
  name               = "${var.cluster_name}"
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
