#!/bin/bash

set -e

echo "Checking all the dependencies..."
# Functions
exists()
{
    command -v "$1" >/dev/null 2>&1
}

# Change directory
echo "Changing to the root folder..."
cd ~

# AWS CLI installation
echo "Checking AWS CLI..."
if ! exists aws ; then 
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install 
else
    sleep 3
    echo "AWS CLI installed, skipping..."
fi

# Git installation
echo "Checking git..."
if ! exists git; then
    sudo apt update
    sudo apt install git-all
else
    sleep 3
    echo "git installed, skipping..."
fi

# Terraform installation
echo "Checking Terraform..."
if ! exists terraform; then
    sudo wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
    sudo apt update && sudo apt install terraform
else
    sleep 3
    echo "Terraform installed, skipping..."
fi

# Done all the installation
echo "Done! Now you can use this repository for developing your first-ever Serverless Web Application!!!"