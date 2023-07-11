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

# Helm Package repository installation
echo "Checking Helm chart..."
if ! exists helm; then
    curl -fsSL "https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3" -o "get_helm.sh" 
    chmod 700 get_helm.sh
    ./get_helm.sh
else
    sleep 3
    echo "Helm installed, skipping..."
fi

# kubectl installation
echo "Checking kubectl..."
if ! exists kubectl; then
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl apt-transport-https
    sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
    echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
    sudo apt-get update
    sudo apt-get install -y kubectl
else
    sleep 3
    echo "kubectl installed, skipping..."
fi

# eksctl installation
echo "Checking eksctl..."
if ! exists eksctl; then
    curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
    sudo mv /tmp/eksctl /usr/local/bin
else
    sleep 3
    echo "eksctl installed, skipping..."
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

# Optional: Install K9s, uncomment this part for installation
# BEGIN with ECHO, ENDING with FI
# echo "Checking K9s..."
# if ! exists k9s; then
#   sudo wget -qO- https://github.com/derailed/k9s/releases/download/v0.26.3/k9s_Linux_x86_64.tar.gz | tar zxvf -  -C /tmp/
#   sudo mv /tmp/k9s /usr/local/bin
# else
#   sleep 3
#   echo "K9s installed, skipping..."
# fi

# Done all the installation
echo "Done! Now you can use this repository for developing your first-ever EKS Cluster with Karpenter!!!"