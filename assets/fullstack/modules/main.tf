data "terraform_remote_state" "db" {
  backend = "s3"

  config = {
    bucket = "${var.db_remote_state_bucket}"
    key    = "${var.db_remote_state_key}"
    region = "us-west-2"
  }
}

resource "aws_default_vpc" "default" {
}

resource "aws_default_subnet" "subnet1" {
  availability_zone = "us-west-2a"
}

resource "aws_default_subnet" "subnet2" {
  availability_zone = "us-west-2b"
}

resource "aws_default_subnet" "subnet3" {
  availability_zone = "us-west-2c"
}

resource "aws_s3_bucket" "webbucket" {
  bucket = "anthony-web-${var.environment}"

  force_destroy = true
}

resource "aws_s3_bucket_object" "object" {
  bucket = aws_s3_bucket.webbucket.id
  key    = "web/application-${var.web_version}.zip"
  source = "${path.module}/../src/application-${var.web_version}.zip"

  force_destroy = true
}

resource "aws_elastic_beanstalk_application" "eb_app" {
  name        = "flask-app-${var.environment}"
  description = "Simple flask app for ${var.environment}"
}

resource "aws_elastic_beanstalk_application_version" "eb_app_ver" {
  bucket      = aws_s3_bucket.webbucket.id
  key         = aws_s3_bucket_object.object.id
  application = aws_elastic_beanstalk_application.eb_app.name
  force_delete = true
  name        = "anthony-app-version-${var.environment}"
}

resource "aws_elastic_beanstalk_environment" "var" {
  name                = "eb-${var.environment}"
  application         = aws_elastic_beanstalk_application.eb_app.name
  solution_stack_name = "64bit Amazon Linux 2 v3.4.0 running Python 3.8"
  description         = "Environment for flask app"
  version_label       = aws_elastic_beanstalk_application_version.eb_app_ver.name

  depends_on = [
    aws_security_group.mysql
  ]

  setting {
    namespace = "aws:ec2:vpc"
    name      = "VPCId"
    value     = "${aws_default_vpc.default.id}"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name = "Subnets"
    value = "${aws_default_subnet.subnet1.id},${aws_default_subnet.subnet2.id},${aws_default_subnet.subnet3.id}"
  }
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "IamInstanceProfile"
    value     = "aws-elasticbeanstalk-ec2-role"
  } 

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t2.micro"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.mysql.id
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MinSize"
    value     = var.min_size
  }

  setting {
    namespace = "aws:autoscaling:asg"
    name      = "MaxSize"
    value     = var.max_size
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "EnvironmentType"
    value     = "LoadBalanced"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "ServiceRole"
    value     = "aws-elasticbeanstalk-service-role"
  }

  setting {
    namespace = "aws:elasticbeanstalk:healthreporting:system"
    name      = "SystemType"
    value     = "enhanced"
  }

  setting {
    namespace = "aws:ec2:vpc"
    name = "ELBSubnets"
    value = "${aws_default_subnet.subnet1.id},${aws_default_subnet.subnet2.id},${aws_default_subnet.subnet3.id}"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_USERNAME"
    value     = "admin"
  }
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_PASSWORD"
    value     = var.db_password
  }
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name = "RDS_DB_NAME"
    value = var.db_name
  }
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "RDS_HOSTNAME"
    value     = var.db_host
  }

}

# resource "aws_default_subnet" "default3" {
#   availability_zone = "us-west-2c"
# }

# data "template_file" "python" {
#   template = file("${path.module}/user-data.json")

#   vars = {
#     "ecs_image_url" = "${var.ecs_image_url}"
#     "db_host"       = "${var.db_host}"
#     "db_password"   = "${var.db_password}"
#   }
# }

# data "template_file" "shell" {
#   template = file("${path.module}/data.sh")
# }

resource "aws_security_group" "mysql" {
  name = "${var.cluster_name}-instance-${var.environment}"

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = [ "0.0.0.0/0" ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

# resource "aws_security_group" "elb" {
#   name = "${var.cluster_name}-elb"
#   ingress {
#     from_port   = 8080
#     to_port     = 8080
#     protocol    = "tcp"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# # Create a ECS Task Definition
# resource "aws_ecs_task_definition" "taskdef" {
#   family                = "ecs-login-app"
#   container_definitions = data.template_file.python.rendered
#   execution_role_arn = aws_iam_role.ecs_task_execution_role.arn
#   network_mode          = "bridge"
# }

# resource "aws_lb" "example" {
#   name               = var.cluster_name
#   load_balancer_type = "application"
#   security_groups    = ["${aws_security_group.elb.id}"]
#   subnets = [ "${aws_default_subnet.default1.id}", "${aws_default_subnet.default2.id}" ]

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_lb_listener" "http" {
#   load_balancer_arn = aws_lb.example.arn
#   port = 8080
#   protocol = "HTTP"

#   default_action {
#     type = "forward"
#     target_group_arn = aws_lb_target_group.example.arn
#   }
# }

# resource "aws_lb_target_group" "example" {
#   port = 8080
#   protocol = "HTTP"
#   vpc_id = aws_default_vpc.default.id

#   health_check {
#     healthy_threshold = 2
#     unhealthy_threshold = 2
#     timeout = 3
#     interval = 30
#     protocol = "HTTP"
#     port = 8080
#     path = "/"
#   }

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_ecs_cluster" "ecs_cluster" {
#   name = "ecs_cluster"

# }

# resource "aws_ecs_service" "service" {
#   name            = var.service_name
#   cluster         = aws_ecs_cluster.ecs_cluster.id
#   task_definition = aws_ecs_task_definition.taskdef.arn
#   desired_count   = var.min_size
#   launch_type     = "EC2"
#   depends_on = [
#     aws_lb_listener.http, aws_iam_role_policy.ecs_task_execution_role
#   ]
#   load_balancer {
#     target_group_arn = aws_lb_target_group.example.arn
#     container_name = "demo-app"
#     container_port = 8080
#   }
# }

# resource "aws_launch_configuration" "example" {
#   image_id = var.ami
#   instance_type = var.instance_type
#   security_groups = ["${aws_security_group.instance.id}"]

#   user_data = data.template_file.shell.rendered
#   iam_instance_profile = aws_iam_instance_profile.ecs.name

#   lifecycle {
#     create_before_destroy = true
#   }
# }

# resource "aws_autoscaling_group" "example" {
#   name = "${var.cluster_name}-${aws_launch_configuration.example.name}"
#   launch_configuration = aws_launch_configuration.example.id

#   availability_zones = [ "us-west-2a", "us-west-2b" ]
#   target_group_arns = ["${aws_lb_target_group.example.arn}"]
#   health_check_type = "ELB"

#   min_size = var.min_size
#   max_size = var.max_size
#   min_elb_capacity = var.min_size

#   lifecycle {
#     create_before_destroy = true
#   }

#   tag {
#     key = "Name"
#     value = "${var.cluster_name}"
#     propagate_at_launch = true
#   }

#   depends_on = [
#     aws_lb.example
#   ]
# }