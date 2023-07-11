#!/bin/bash
set -e

cd ~/code/terraform/learn-terraform-provision-eks-cluster
echo "Terraform initializing..."

terraform init
terraform fmt
terraform validate
terraform plan
terraform apply

echo "Retrieving access..."
rm -rf ~/.kube/config
aws eks --region $(terraform output -raw region) update-kubeconfig --name $(terraform output -raw cluster_name)

echo "Checking information..."
kubectl cluster-info
kubectl get nodes

echo "Cleaning workspace..."
terraform destroy