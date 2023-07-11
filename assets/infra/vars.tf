variable "region" {
  description = "AWS Region"
  default = "us-west-2"
}

variable "vpc_cidr" {
  default = "10.0.0.0/16"
}

variable "subnet1_cidr" {
  default = "10.0.1.0/24"
}
