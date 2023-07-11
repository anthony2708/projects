#!/bin/bash

set -e

EKSVERSION=$(eksctl version) 
echo "EKS Version is ${EKSVERSION}"

# Deploy VPC Resource controller
echo "Deploy Resource Controller"
eksctl utils install-vpc-controllers --cluster eksworkshop-eksctl --approve

# Setup windows node
echo "Setup Windows Node"
mkdir ~/code/k8s/windows
cat << EoF > ~/code/k8s/windows/windows_nodes.yaml
apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: eksworkshop-eksctl
  region: ${AWS_REGION}

nodeGroups:
  - name: windows-ng
    amiFamily: WindowsServer2019CoreContainer
    desiredCapacity: 1
    instanceType: t2.large
    ssh:
      enableSsm: true
EoF

# Run the configuration
echo "Creating nodegroup..."
eksctl create nodegroup -f ~/code/k8s/windows/windows_nodes.yaml

echo "Checking nodes..."
kubectl get nodes -l kubernetes.io/os=windows -L kubernetes.io/os
