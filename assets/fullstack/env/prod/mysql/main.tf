provider "aws" {
  region = "us-west-2"
}

resource "aws_security_group" "mysql" {
  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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

resource "aws_db_instance" "example" {
  engine                 = "mysql"
  allocated_storage      = 10
  instance_class         = "db.t2.micro"
  db_name                = "anthony_terraform_prod"
  username               = "admin"
  password               = var.db_password
  vpc_security_group_ids = ["${aws_security_group.mysql.id}"]
  publicly_accessible    = true
  skip_final_snapshot    = true
}   