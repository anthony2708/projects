#!/bin/bash

set -e

export $AWS_ACCESS_KEY_ID=$1
export $AWS_SECRET_ACCESS_KEY=$2

cd ../includes

terraform init
terraform fmt
terraform validate
terraform plan -var="aws_access_key=$AWS_ACCESS_KEY_ID" -var="aws_secret_key=$AWS_SECRET_ACCESS_KEY"
terraform apply -auto-approve -var="aws_access_key=$AWS_ACCESS_KEY_ID" -var="aws_secret_key=$AWS_SECRET_ACCESS_KEY"
