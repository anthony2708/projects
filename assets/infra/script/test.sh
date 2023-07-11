#!/bin/bash
set -e

echo "Testing locking..."
cd ~/code/assets/test
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply