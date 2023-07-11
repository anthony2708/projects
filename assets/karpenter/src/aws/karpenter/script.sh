#!/bin/bash

set -e

KARPENTER_VERSION=v0.16.0
CLUSTER_NAME=$(eksctl get clusters -o json | jq -r '.[0].Name')
ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
AWS_REGION=$(aws configure get region)

echo "Deploying CloudFormation stack..."
TEMPOUT=$(mktemp)
curl -fsSL https://karpenter.sh/"${KARPENTER_VERSION}"/getting-started/getting-started-with-eksctl/cloudformation.yaml  > $TEMPOUT \
&& aws cloudformation deploy \
  --stack-name "Karpenter-${CLUSTER_NAME}" \
  --template-file "${TEMPOUT}" \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides "ClusterName=${CLUSTER_NAME}"

echo "Creating IAM Identity Mapping..."
eksctl create iamidentitymapping \
  --username system:node:{{EC2PrivateDNSName}} \
  --cluster  ${CLUSTER_NAME} \
  --arn "arn:aws:iam::${ACCOUNT_ID}:role/KarpenterNodeRole-${CLUSTER_NAME}" \
  --group system:bootstrappers \
  --group system:nodes

echo "Checking Configuration Map..."
kubectl describe configmap -n kube-system aws-auth

echo "Creating OIDC Provider and assigning to IAM Service Account"
eksctl utils associate-iam-oidc-provider --cluster ${CLUSTER_NAME} --approve
eksctl create iamserviceaccount \
  --cluster "${CLUSTER_NAME}" --name karpenter --namespace karpenter \
  --role-name "${CLUSTER_NAME}-karpenter" \
  --attach-policy-arn "arn:aws:iam::${ACCOUNT_ID}:policy/KarpenterControllerPolicy-${CLUSTER_NAME}" \
  --role-only \
  --approve

export KARPENTER_IAM_ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${CLUSTER_NAME}-karpenter"

echo "Creating EC2 Spot Linked Role..."
aws iam create-service-linked-role --aws-service-name spot.amazonaws.com

echo "Installing Karpenter in a namespace..."
helm repo add karpenter https://charts.karpenter.sh/
helm repo update
helm upgrade --install --namespace karpenter --create-namespace \
  karpenter karpenter/karpenter --version ${KARPENTER_VERSION} \
  --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"=${KARPENTER_IAM_ROLE_ARN} \
  --set clusterName=${CLUSTER_NAME} \
  --set clusterEndpoint=$(aws eks describe-cluster --name ${CLUSTER_NAME} --query "cluster.endpoint" --output json) \
  --set defaultProvisioner.create=false \
  --set aws.defaultInstanceProfile=KarpenterNodeInstanceProfile-${CLUSTER_NAME} \
  --wait # for the defaulting webhook to install before creating a Provisioner

echo "Checking all resources..."
kubectl get all -n karpenter
kubectl get deployment -n karpenter
kubectl get pods --namespace karpenter
kubectl get pod -n karpenter --no-headers | awk '{print $1}' | head -n 1 | xargs kubectl describe pod -n karpenter

echo "Applying Karpenter..."
kubectl apply -f karpenter.yaml

echo "Deploying Application..."
kubectl apply -f inflate.yaml

echo "DONE!!!"
