output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server_anthonytest.id
}

output "instance_public_ip" {
  description = "Public IP Address of the EC2 Instance"
  value       = aws_instance.app_server_anthonytest.public_ip
}