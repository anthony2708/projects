# Terraform for AWS and K8s

*From 06th September 2022*

## Install the required dependencies

```bash
# Update & Install gnupg, software-properties-common
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

# Install the Hashicorp GPG Key
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Verify the fingerprint
gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint

# Add repository to system
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list

# Install Terraform
sudo apt update && sudo apt-get install terraform

# Check for existence
terraform -help

# Tab completion
if [ ! -f ~/.bashrc ]; then
    touch ~/.bashrc
fi

terraform -install-autocomplete
```

## Build infrastructure with AWS

```bash
# Export AWS_ACCESS_KEY_ID & AWS_SECRET_ACCESS_KEY

# Create a template
mkdir learn-terraform-aws-instance
cd learn-terraform-aws-instance
touch main.tf
```

```h
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = "us-west-2"
}

resource "aws_instance" "app_server" {
  ami           = "ami-830c94e3"
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleAppServerInstance"
  }
}
```

```bash
# Format and validate. then apply
terraform fmt
terraform validate
terraform plan
terraform apply

# CHECK FOR STATES
terraform show
terraform state list
terraform destroy
```

## Define input values & output values
```bash
# Create a file. then check for modify
touch variables.tf
touch outputs.tf

terraform fmt
terraform validate
terraform plan
terraform apply
terraform destroy
```

```h
variable "instance_name" {
  description = "Value of the Name tag for the EC2 instance"
  type        = string
  default     = "ExampleAppServerInstance"
}
```

```h
output "instance_id" {
  description = "ID of the EC2 instance"
  value       = aws_instance.app_server.id
}

output "instance_public_ip" {
  description = "Public IP address of the EC2 instance"
  value       = aws_instance.app_server.public_ip
}
```