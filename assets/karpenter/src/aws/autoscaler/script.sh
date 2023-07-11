#!/bin/bash

set -e

export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export ASG_NAME=$(aws autoscaling describe-auto-scaling-groups --query "AutoScalingGroups[? Tags[? (Key=='eks:cluster-name') \
        && Value=='eksworkshop-eksctl']].AutoScalingGroupName" --output text)

echo "Updating the Autoscaling Group..."
aws autoscaling update-auto-scaling-group \
    --auto-scaling-group-name ${ASG_NAME} \
    --min-size 3 --desired-capacity 3  --max-size 4

echo "Creating OIDC Provider..."
eksctl utils associate-iam-oidc-provider --cluster eksworkshop-eksctl --approve

echo "Creating policy and attaching to IAM Service Account..."
aws iam create-policy   \
  --policy-name k8s-asg-policy \
  --policy-document file://policy.json

eksctl create iamserviceaccount \
    --name cluster-autoscaler \
    --namespace kube-system \
    --cluster eksworkshop-eksctl \
    --attach-policy-arn "arn:aws:iam::${ACCOUNT_ID}:policy/k8s-asg-policy" \
    --approve --override-existing-serviceaccounts

kubectl -n kube-system describe sa cluster-autoscaler

echo "Deploying CAS..."
kubectl apply -f autoscaler.yaml

kubectl -n kube-system \
    annotate deployment.apps/cluster-autoscaler \
    cluster-autoscaler.kubernetes.io/safe-to-evict="false"

export K8S_VERSION=$(kubectl version --short | grep 'Server Version:' | sed 's/[^0-9.]*\([0-9.]*\).*/\1/' | cut -d. -f1,2)
export AUTOSCALER_VERSION=$(curl -s "https://api.github.com/repos/kubernetes/autoscaler/releases" | grep '"tag_name":' | sed \ 
        -s 's/.*-\([0-9][0-9\.]*\).*/\1/' | grep -m1 ${K8S_VERSION})

echo "Updating the images..."
kubectl -n kube-system \
    set image deployment.apps/cluster-autoscaler \
    cluster-autoscaler=us.gcr.io/k8s-artifacts-prod/autoscaling/cluster-autoscaler:v${AUTOSCALER_VERSION}

echo "Deploying application and scaling..."
kubectl apply -f nginx.yaml
kubectl scale --replicas=10 deployment/nginx-to-scaleout

echo "Checking results..."
kubectl get pods -l app=nginx -o wide
kubectl get nodes

echo "DONE!!!"