#!/bin/bash

set -e

export $ENVIRONMENT=$1
export $AWS_ACCESS_KEY_ID=$2
export $AWS_SECRET_ACCESS_KEY=$3

cd ../aws

terraform init
terraform workspace new $ENVIRONMENT || terraform workspace select $ENVIRONMENT
terraform fmt
terraform validate
terraform plan -var="aws_access_key=$AWS_ACCESS_KEY_ID" -var="aws_secret_key=$AWS_SECRET_ACCESS_KEY"
terraform apply -auto-approve -var="aws_access_key=$AWS_ACCESS_KEY_ID" -var="aws_secret_key=$AWS_SECRET_ACCESS_KEY"
