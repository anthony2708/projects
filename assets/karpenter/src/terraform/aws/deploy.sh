#!/bin/bash

set -e

echo "==> Applying..."
terraform apply -var "aws_access_key=$AWS_ACCESS_KEY_ID" -var "aws_secret_key=$AWS_SECRET_ACCESS_KEY" -auto-approve -input=false

echo "DONE!!!"