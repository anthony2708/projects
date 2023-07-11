resource "aws_instance" "demo_ec2" {
  count         = 1
  instance_type = "t2.micro"
  ami           = "ami-830c94e3"
  tags = {
    "Name" = "demo_ec2-${count.index}"
  }
}