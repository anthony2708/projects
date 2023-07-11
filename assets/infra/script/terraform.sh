#!/bin/bash

# Script use to define multiple environments for AWS + Terraform
# Developed by Anh T.Bui - SRE Intern at OPSWAT Vietnam
# Please use this script with careful consideration.

set -e

AWS_ACCESS_KEY_ID=$1
AWS_SECRET_ACCESS_KEY=$2
AWS_REGION=$3
AWS_OUTPUT=$4

# Prequesities
echo "Installing AWSCLI..."
if [ ! aws ]; then
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    rm awscliv2.zip
fi

echo "Installing Terraform..."
# TODO: Develop new installation with more Linux Distro
# If using Windows, please switch to WSL2

if [ $(cat /etc/*release | grep Ubuntu) ]; then
    echo "==> Step 1: Install dependencies..."
    sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

    echo "==> Step 2: Installing Hashicorp GPG Key..."
    wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

    echo "==> Step 3: Verifying the key,,,"
    gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint

    echo "==> Step 4: Adding the repository..."
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list

    echo "==> Step 5: Downloading & Installing Terraform..."
    sudo apt update
    sudo apt-get install terraform
fi

echo "Checking AWS CLI & Terraform version"
aws --version
terrafrom -version

echo "Enabling tab completion..."
touch ~/.bashrc
terraform -install-autocomplete

if [ ! -n "$1" ] && [ ! -n "$2" ]; then
    echo "You did not provide enough credentials for AWS"
    exit 1
fi

echo "Configurating AWS Credentials..."
aws configure set aws_access_key_id "$1"
aws configure set aws_secret_access_key "$2"
aws configure set region "$3"

if [ "$4" = "yaml" ] || [ "$4" = "yaml-stream" ] || [ "$4" = "text" ] || [ "$4" = "table" ]; then
    aws configure set output "$4"
else
    aws configure set output "json"
fi