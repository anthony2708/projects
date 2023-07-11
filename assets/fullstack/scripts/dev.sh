#!/bin/bash

set -e

echo "AWS MySQL initializing..."
cd ../env/dev/mysql
terraform fmt
terraform init
terraform validate
terraform plan -var "aws_access_key_id=$AWS_ACCESS_KEY_ID" -var "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" -var "db_password=$DATABASE_PASSWORD" 
terraform apply -var "aws_access_key_id=$AWS_ACCESS_KEY_ID" -var "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" -var "db_password=$DATABASE_PASSWORD" \
                -auto-approve --input=false 
unset TF_VAR_db_host
export TF_VAR_db_host=$(terraform output -raw addr)

echo "Flask application initializing..."
echo "==> Step 1: Zipping files..."
cd ../../../src
if [ -f application-v*.zip ]; then
    rm application-v*.zip
fi
zip application-v$BITBUCKET_BUILD_NUMBER.zip application.py static/* templates/* requirements.txt

echo "==> Step 2: Terraform initialization..."
cd ../env/dev/services
terraform fmt
terraform init
terraform validate
terraform plan -var "aws_access_key_id=$AWS_ACCESS_KEY_ID" -var "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" \
                -var "db_password=$DATABASE_PASSWORD" -var "web_version=v$BITBUCKET_BUILD_NUMBER"
terraform apply -var "aws_access_key_id=$AWS_ACCESS_KEY_ID" -var "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" \
                -var "db_password=$DATABASE_PASSWORD" -var "web_version=v$BITBUCKET_BUILD_NUMBER" \
                -auto-approve --input=false 

echo "==> Step 3: Confirm the process done"
cd ../../../
echo "----------DONE-----------"