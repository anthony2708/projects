#!/bin/bash

set -e

# GNUPG & Software-properties-common
echo "GNUPG & Software installing..."
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common

# Install Hashicorp GPG Key
echo "Installing keys..."
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Verify the fingerprint
echo "Verifying the fingerprint..."
gpg --no-default-keyring \
    --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg \
    --fingerprint

# Add repository to system
echo "Adding the repository to the system..."
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list

# Install Terraform
echo "Installing Terraform..."
sudo apt update && sudo apt-get install terraform

# Check for existence
echo "Checking for terraform in the system"
terraform -help

# Tab completion
if [ ! -f ~/.bashrc ]; then
    touch ~/.bashrc
fi

terraform -install-autocomplete