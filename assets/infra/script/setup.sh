#!/bin/bash
set -e

echo "Setting up files with Terraform..."
echo "==> Step 1: Create a AWS DynamoDB Table"
cd ~/code/assets/server
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply

echo "==> Step 2: Check locking"
cd ~/code/assets/test
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply