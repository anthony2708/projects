#!/bin/bash

set -e

echo "==> Formatting..."
terraform fmt

echo "==> Initializing..."
terraform init

echo "==> Validating and Planning..."
terraform validate
terraform plan -var "aws_access_key=$AWS_ACCESS_KEY_ID" -var "aws_secret_key=$AWS_SECRET_ACCESS_KEY"

# echo "==> Applying..."
# terraform apply -var "aws_access_key=$AWS_ACCESS_KEY_ID" -var "aws_secret_key=$AWS_SECRET_ACCESS_KEY" -auto-approve -input=false

echo "DONE!!!"