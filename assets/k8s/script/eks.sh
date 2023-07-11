#!/bin/bash

set -e

# Setup region
AWS_REGION=($(aws configure get region))
AZS=($(aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName' --output text --region $AWS_REGION))
test -n "$AWS_REGION" && echo AWS_REGION is "$AWS_REGION" || echo AWS_REGION is not set

# Create the cluster with the information
if [ -f ~/code/k8s/aws/eksworkshop.yaml ]; then
    echo "Removing old files..."
    rm -rf ~/code/k8s/aws/eksworkshop.yaml
fi

echo "Writing new configuration..."
cat << EOF > ~/code/k8s/aws/eksworkshop.yaml
---
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: eksworkshop-eksctl
  region: ${AWS_REGION}
  version: "1.21"

availabilityZones: ["${AZS[0]}", "${AZS[1]}", "${AZS[2]}"]

managedNodeGroups:
- name: nodegroup
  desiredCapacity: 3
  instanceType: t3.micro
  ssh:
    enableSsm: true

# To enable all of the control plane logs, uncomment below:
# cloudWatch:
#  clusterLogging:
#    enableTypes: ["*"]

# secretsEncryption:
#  keyARN: ${MASTER_ARN}
EOF

# Run the program, wait for 15 minutes
echo "Running the configuration..."
eksctl create cluster -f ~/code/k8s/aws/eksworkshop.yaml

# Check for errors and grant permission to interact
echo "Getting nodes..."
kubectl get nodes 

echo "Updating region..."
aws eks update-kubeconfig --name eksworkshop-eksctl --region ${AWS_REGION}
