#!/bin/bash

set -e

echo "Creating KarpenterInstanceNodeRole and attaching policies..."
aws iam create-role --role-name KarpenterInstanceNodeRole \
    --assume-role-policy-document file://json/node_policy.json

aws iam attach-role-policy --role-name KarpenterInstanceNodeRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy

aws iam attach-role-policy --role-name KarpenterInstanceNodeRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy

aws iam attach-role-policy --role-name KarpenterInstanceNodeRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly

aws iam attach-role-policy --role-name KarpenterInstanceNodeRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore

echo "Creating KarpenterInstanceProfile and adding roles..."
aws iam create-instance-profile \
    --instance-profile-name KarpenterInstanceProfile

aws iam add-role-to-instance-profile \
    --instance-profile-name KarpenterInstanceProfile \
    --role-name KarpenterInstanceNodeRole

echo "Assigning variables..."
CLUSTER_NAME=eksworkshop-eksctl
CLUSTER_ENDPOINT="$(aws eks describe-cluster \
    --name ${CLUSTER_NAME} --query "cluster.endpoint" \
    --output text)"
OIDC_ENDPOINT="$(aws eks describe-cluster --name ${CLUSTER_NAME} \
    --query "cluster.identity.oidc.issuer" --output text)"
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' \
    --output text)

echo "Creating KarpenterControllerRole and attaching policy..."
aws iam create-role --role-name KarpenterControllerRole-${CLUSTER_NAME} \
    --assume-role-policy-document file://json/controller_trust.json

aws iam put-role-policy --role-name KarpenterControllerRole-${CLUSTER_NAME} \
    --policy-name KarpenterControllerPolicy-${CLUSTER_NAME} \
    --policy-document file://json/controller_policy.json


echo "Adding tags to Subnets..."
for NODEGROUP in $(aws eks list-nodegroups --cluster-name ${CLUSTER_NAME} \
    --query 'nodegroups' --output text); do 
    aws ec2 create-tags \
        --tags "Key=karpenter.sh/discovery,Value=${CLUSTER_NAME}" \
        --resources $(aws eks describe-nodegroup --cluster-name ${CLUSTER_NAME} \
        --nodegroup-name $NODEGROUP --query 'nodegroup.subnets' --output text )
done

echo "Adding tags to Security groups..."
NODEGROUP=$(aws eks list-nodegroups --cluster-name ${CLUSTER_NAME} \
    --query 'nodegroups[0]' --output text)

LAUNCH_TEMPLATE=$(aws eks describe-nodegroup --cluster-name ${CLUSTER_NAME} \
    --nodegroup-name ${NODEGROUP} --query 'nodegroup.launchTemplate.{id:id,version:version}' \
    --output text | tr -s "\t" ",")

SECURITY_GROUPS=$(aws ec2 describe-launch-template-versions \
    --launch-template-id ${LAUNCH_TEMPLATE%,*} --versions ${LAUNCH_TEMPLATE#*,} \
    --query 'LaunchTemplateVersions[0].LaunchTemplateData.[NetworkInterfaces[0].Groups||SecurityGroupIds]' \
    --output text)

aws ec2 create-tags \
    --tags "Key=karpenter.sh/discovery,Value=${CLUSTER_NAME}" \
    --resources ${SECURITY_GROUPS}

echo "Creating EC2 Spot Linked Role"
aws iam create-service-linked-role --aws-service-name spot.amazonaws.com

echo "Creating Karpenter configuraion and applying..."
export KARPENTER_VERSION=v0.18.1
helm template karpenter oci://public.ecr.aws/karpenter/karpenter --version ${KARPENTER_VERSION} --namespace karpenter \
    --set aws.defaultInstanceProfile=KarpenterInstanceProfile \
    --set clusterEndpoint="${CLUSTER_ENDPOINT}" \
    --set clusterName=${CLUSTER_NAME} \
    --set serviceAccount.annotations."eks\.amazonaws\.com/role-arn"="arn:aws:iam::${ACCOUNT_ID}:role/KarpenterControllerRole-${CLUSTER_NAME}" \
    --version ${KARPENTER_VERSION} > config/karpenter.yaml

kubectl create namespace karpenter
kubectl create -f \
    https://raw.githubusercontent.com/aws/karpenter/${KARPENTER_VERSION}/charts/karpenter/crds/karpenter.sh_provisioners.yaml
kubectl apply -f config/karpenter.yaml

echo "Applying Provisioner and Pod Disruption Budget configuration..."
kubectl apply -f config/provisioner.yaml
kubectl apply -f config/pdb.yaml

echo "Scaling down the Autoscaler, moving to Karpenter..."
kubectl scale deploy/cluster-autoscaler -n kube-system --replicas=0
aws eks update-nodegroup-config --cluster-name ${CLUSTER_NAME} \
    --nodegroup-name ${NODEGROUP} \
    --scaling-config "minSize=2,maxSize=2,desiredSize=2"

echo "DONE!"