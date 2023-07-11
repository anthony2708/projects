# K8s & AWS - Elastic Kubenetes Service

## Prerequisites
***Call all the functions with bash (Linux Distro or WSL2 + Ubuntu 20.04 needed)***

## Install Dependencies
```bash
# Update the package management
sudo apt update
sudo apt upgrade

# Kubectl
sudo curl --silent --location -o /usr/local/bin/kubectl \
   https://s3.us-west-2.amazonaws.com/amazon-eks/1.21.5/2022-01-21/bin/linux/amd64/kubectl # Turn off silent for progress

sudo chmod +x /usr/local/bin/kubectl

# AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# JQ, ENVSubset. YQ
sudo yum -y install jq gettext bash-completion moreutils
echo 'yq() {
  docker run --rm -i -v "${PWD}":/workdir mikefarah/yq "$@"
}' | tee -a ~/.bashrc && source ~/.bashrc

# Validation
for command in kubectl jq envsubst aws
  do
    which $command &>/dev/null && echo "$command in path" || echo "$command NOT FOUND"
  done

# Bash completion
kubectl completion bash >>  ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion

# Load balancer version
echo 'export LBC_VERSION="v2.4.1"' >>  ~/.bash_profile
echo 'export LBC_CHART_VERSION="1.4.1"' >>  ~/.bash_profile
.  ~/.bash_profile
```

## Setup regions/ID/AZs
```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --output text --query Account)
export AWS_REGION=$(curl -s 169.254.169.254/latest/dynamic/instance-identity/document | jq -r '.region') # May have errors --> ec2 instance needed
export AZS=($(aws ec2 describe-availability-zones --query 'AvailabilityZones[].ZoneName' --output text --region $AWS_REGION))

test -n "$AWS_REGION" && echo AWS_REGION is "$AWS_REGION" || echo AWS_REGION is not set

echo "export ACCOUNT_ID=${ACCOUNT_ID}" | tee -a ~/.bash_profile
echo "export AWS_REGION=${AWS_REGION}" | tee -a ~/.bash_profile
echo "export AZS=(${AZS[@]})" | tee -a ~/.bash_profile
aws configure set default.region ${AWS_REGION}
aws configure get default.region
```

## Clone repo
```bash
cd ~/code
git clone https://github.com/aws-containers/ecsdemo-frontend.git
git clone https://github.com/aws-containers/ecsdemo-nodejs.git
git clone https://github.com/aws-containers/ecsdemo-crystal.git
```

## Validate IAM (Cloud9)
```bash
aws sts get-caller-identity
aws sts get-caller-identity --query Arn | grep eksworkshop-admin -q && echo "IAM role valid" || echo "IAM role NOT valid"
```

## Setup eksctl
```bash
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sudo mv -v /tmp/eksctl /usr/local/bin

eksctl version

eksctl completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
```

## Create cluster
```bash
eksctl create cluster -f eksworkshop.yaml

kubectl get nodes # if we see our 3 nodes, we know we have authenticated correctly
```

## Update config
```bash
aws eks update-kubeconfig --name eksworkshop-eksctl --region ${AWS_REGION}

STACK_NAME=$(eksctl get nodegroup --cluster eksworkshop-eksctl -o json | jq -r '.[].StackName')

ROLE_NAME=$(aws cloudformation describe-stack-resources --stack-name $STACK_NAME | jq -r '.StackResources[] | select(.ResourceType=="AWS::IAM::Role") | .PhysicalResourceId')

echo "export ROLE_NAME=${ROLE_NAME}" | tee -a ~/.bash_profile
```

## Deploy application
```bash
cd ~/code/ecsdemo-frontend

kubectl apply -f kubernetes/service.yaml

kubectl apply -f kubernetes/deployment.yaml
```
```bash
cd ~/code/ecsdemo-crystal

kubectl apply -f kubernetes/service.yaml

kubectl apply -f kubernetes/deployment.yaml
```
```bash
cd ~/code/ecsdemo-nodejs

kubectl apply -f kubernetes/service.yaml

kubectl apply -f kubernetes/deployment.yaml
```
```bash
kubectl get deployment ecsdemo-nodejs

kubectl get deployment ecsdemo-crystal

kubectl get deployment ecsdemo-frontend
```
## Check frontend
```bash
kubectl get service ecsdemo-frontend -o wide

ELB=$(kubectl get service ecsdemo-frontend -o json | jq -r '.status.loadBalancer.ingress[].hostname)

curl -m3 -v $ELB
```

## Scale deployments
```bash
kubectl get deployments

kubectl scale deployment ecsdemo-nodejs --replicas=3

kubectl scale deployment ecsdemo-crystal --replicas=3

kubectl scale deployment ecsdemo-frontend --replicas=3
```

## Cleanup
```bash
cd ~/code/ecsdemo-frontend

kubectl delete -f kubernetes/service.yaml

kubectl delete -f kubernetes/deployment.yaml

cd ~/code/ecsdemo-crystal

kubectl delete -f kubernetes/service.yaml

kubectl delete -f kubernetes/deployment.yaml

cd ~/code/ecsdemo-nodejs

kubectl delete -f kubernetes/service.yaml

kubectl delete -f kubernetes/deployment.yaml

export DASHBOARD_VERSION="v2.0.0"

kubectl delete -f https://raw.githubusercontent.com/kubernetes/dashboard/${DASHBOARD_VERSION}/src/deploy/recommended/kubernetes-dashboard.yaml

eksctl delete cluster --name=eksworkshop-eksctl
```

# Helm

## Microservices

### Create a chart
```bash
helm create eksdemo
```

### Setup
```bash
rm -rf ~/code/eksdemo/templates/

rm ~/code/eksdemo/Chart.yaml

rm ~/code/eksdemo/values.yaml
```
```bash
cat <<EoF > ~/code/eksdemo/Chart.yaml
apiVersion: v2
name: eksdemo
description: A Helm chart for EKS Workshop Microservices application
version: 0.1.0
appVersion: 1.0
EoF
```

### Deploy & Check
```bash
helm install --debug --dry-run workshop ~/code/eksdemo

helm install workshop ~/code/eksdemo --> Real

helm install workshop ~/code/eksdemo

kubectl get svc ecsdemo-frontend -o jsonpath="{.status.loadBalancer.ingress[*].hostname}"; echo
```
### Update & Rollback. Uninstall the pods
```bash
helm upgrade workshop ~/code/eksdemo

helm history workshop

helm rollback workshop 1

helm uninstall workshop
```

### Create subfolders for each template type
```bash
mkdir -p ~/code/eksdemo/templates/deployment

mkdir -p ~/code/eksdemo/templates/service
```
```bash
### Copy and rename frontend manifests
cp ~/code/ecsdemo-frontend/kubernetes/deployment.yaml ~/code/eksdemo/templates/deployment/frontend.yaml

cp ~/code/ecsdemo-frontend/kubernetes/service.yaml ~/code/eksdemo/templates/service/frontend.yaml

### Copy and rename crystal manifests
cp ~/code/ecsdemo-crystal/kubernetes/deployment.yaml ~/code/eksdemo/templates/deployment/crystal.yaml

cp ~/code/ecsdemo-crystal/kubernetes/service.yaml ~/code/eksdemo/templates/service/crystal.yaml

### Copy and rename nodejs manifests
cp ~/code/ecsdemo-nodejs/kubernetes/deployment.yaml ~/code/eksdemo/templates/deployment/nodejs.yaml

cp ~/code/ecsdemo-nodejs/kubernetes/service.yaml ~/code/eksdemo/templates/service/nodejs.yaml
```
### Change the variables to template directives
```yaml
replicas: {{ .Values.replicas }}

frontend --> - image: {{ .Values.frontend.image }}:{{ .Values.version }}

crystal --> - image: {{ .Values.crystal.image }}:{{ .Values.version }}

nodejs --> 	- image: {{ .Values.nodejs.image }}:{{ .Values.version }}
```
### Template directives
```bash
cat <<EoF > ~/code/eksdemo/values.yaml
# Default values for eksdemo.
# This is a YAML-formatted file.
# Declare variables to be passed into your templates.

# Release-wide Values
replicas: 3
version: 'latest'

# Service Specific Values
nodejs:
  image: brentley/ecsdemo-nodejs
crystal:
  image: brentley/ecsdemo-crystal
frontend:
  image: brentley/ecsdemo-frontend
EoF
```

## Nginx

### Install Helm CLI
```bash
curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

helm version --short
```
### Add stable repo
```bash
helm repo add stable https://charts.helm.sh/stable

helm search repo stable
```
### Bash Completion
```bash
helm completion bash >> ~/.bash_completion

. /etc/profile.d/bash_completion.sh

. ~/.bash_completion

source <(helm completion bash)
```
### Update repo
```bash
# first, add the default repository, then update
helm repo add stable https://charts.helm.sh/stable

helm repo update
```
### Add Bitnami
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami

helm install webserver bitnami/nginx
```
### Check for Pods
```bash
kubectl get svc,po,deploy

kubectl describe deployment webserver

kubectl get pods -l app.kubernetes.io/name=nginx

kubectl get service webserver-nginx -o wide
```
### Cleanup
```bash
helm uninstall webserver
```

# App Mesh (DJ App)

## Backend
```bash
kubectl apply -f 1_base_application/base_app.yaml

kubectl -n prod get all
```

## Test services (Ctrl + D to exit)
```bash
export DJ_POD_NAME=$(kubectl get pods -n prod -l app=dj -o jsonpath='{.items[].metadata.name}')

kubectl exec -n prod -it ${DJ_PROD_NAME} bash

curl -s jazz-v1:9080 | json_pp

curl -s metal-v1:9080 | json_pp
```

## Integration
```bash
helm repo add eks https://aws.github.io/eks-charts

helm repo list | grep eks-charts
```

```bash
kubectl create ns appmesh-system

# Create your OIDC identity provider for the cluster
eksctl utils associate-iam-oidc-provider --cluster eksworkshop-eksctl --approve

# Download the IAM policy document for the controller
curl -o controller-iam-policy.json https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/master/config/iam/controller-iam-policy.json

# Create an IAM policy for the controller from the policy document
aws iam create-policy --policy-name AWSAppMeshK8sControllerIAMPolicy --policy-document file://controller-iam-policy.json

# Create an IAM role and service account for the controller
eksctl create iamserviceaccount --cluster eksworkshop-eksctl --namespace appmesh-system \
  --name appmesh-controller \
  --attach-policy-arn arn:aws:iam::$ACCOUNT_ID:policy/AWSAppMeshK8sControllerIAMPolicy  \
  --override-existing-serviceaccounts --approve

# Upgrade charts
helm upgrade -i appmesh-controller eks/appmesh-controller \
  --namespace appmesh-system \
  --set region=${AWS_REGION} \
  --set serviceAccount.create=false \
  --set serviceAccount.name=appmesh-controller
```
## Check for working
```bash
kubectl -n appmesh-system get all

kubectl get crds | grep appmesh
```

## Creating the meshed application
```bash
kubectl apply -f 2_meshed_application/meshed_app.yaml

kubectl get meshes

aws appmesh list-meshes

kubectl get all -n prod
```

## Sidecar Injection
```bash
# Download the IAM policy document for the Envoy proxies
curl -o envoy-iam-policy.json https://raw.githubusercontent.com/aws/aws-app-mesh-controller-for-k8s/master/config/iam/envoy-iam-policy.json

# Create an IAM policy for the proxies from the policy document
aws iam create-policy --policy-name AWSAppMeshEnvoySidecarIAMPolicy --policy-document file://envoy-iam-policy.json

# Create an IAM role and service account for the application namespace
eksctl create iamserviceaccount --cluster eksworkshop-eksctl --namespace prod --name default \
  --attach-policy-arn arn:aws:iam::$ACCOUNT_ID:policy/AWSAppMeshEnvoySidecarIAMPolicy  \
  --override-existing-serviceaccounts --approve

kubectl get pods -n prod

kubectl -n prod rollout restart deployment dj jazz-v1 metal-v1
```

## Check for some changes
```bash
export DJ_POD_NAME=$(kubectl get pods -n prod -l app=dj -o jsonpath='{.items[].metadata.name}')

kubectl -n prod get pods $DJ_POD_NAME -o jsonpath='{.spec.containers[*].name}'

kubectl -n prod exec -it ${DJ_POD_NAME} -c dj bash
```

```bash
curl -s jazz.prod.svc.cluster.local:9080 | json_pp
curl -s jazz.prod.svc.cluster.local:9080 | json_pp
```

## Canary Testing --> Slow exposing new version (v2)
```bash
kubectl apply -f 3_canary_new_version/v2_app.yaml
kubectl -n prod get deployments,services,virtualnodes,virtualrouters
kubectl -n prod describe virtualrouters jazz-router
```

## Testing application
```bash
# Some errors occured when retesting the application (limited resouces + some unexpected reasons, in investigation)
while true; do
  curl http://jazz.prod.svc.cluster.local:9080/
  echo
  sleep .5
done

while true; do
  curl http://metal.prod.svc.cluster.local:9080/
  echo
  sleep .5
done
```

## Cleanup
```bash
kubectl delete namespace prod
kubectl delete meshes dj-app
helm -n appmesh-system delete appmesh-controller

for i in $(kubectl get crd | grep appmesh | cut -d" " -f1) ; do
kubectl delete crd $i
done

kubectl delete namespace appmesh-system
eksctl delete iamserviceaccount --cluster eksworkshop-eksctl --namespace appmesh-system --name appmesh-controller
eksctl delete iamserviceaccount --cluster eksworkshop-eksctl --namespace prod --name default
```

# EKS Fargate (2048 Game)

## Create a profile
```bash
eksctl create fargateprofile --cluster eksworkshop-eksctl --name game-2048 --namespace game-2048

eksctl get fargateprofile --cluster eksworkshop-eksctl -o yaml
```

## Load Balancer Controller

**Requirements: Helm installed**

```bash
eksctl utils associate-iam-oidc-provider --region ${AWS_REGION} --cluster eksworkshop-eksctl --approve

# IAM Policy
curl -o iam_policy.json https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/${LBC_VERSION}/docs/install/iam_policy.json

aws iam create-policy --policy-name AWSLoadBalancerControllerIAMPolicy --policy-document file://iam_policy.json

rm iam_policy.json

# IAM Role
eksctl create iamserviceaccount --cluster eksworkshop-eksctl --namespace kube-system \
  --name aws-load-balancer-controller \
  --attach-policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/AWSLoadBalancerControllerIAMPolicy \
  --override-existing-serviceaccounts --approve

kubectl get sa aws-load-balancer-controller -n kube-system -o yaml

# Install the TargetGroupBinding CRDs
kubectl apply -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller/crds?ref=master"

# Deploy the Helm chart from the Amazon EKS charts repo
if [ ! -x ${LBC_VERSION} ]
  then
    tput setaf 2; echo '${LBC_VERSION} has been set.'
  else
    tput setaf 1;echo '${LBC_VERSION} has NOT been set.'
fi
helm repo add eks https://aws.github.io/eks-charts

export VPC_ID=$(aws eks describe-cluster --name eksworkshop-eksctl --query "cluster.resourcesVpcConfig.vpcId" --output text)

helm upgrade -i aws-load-balancer-controller eks/aws-load-balancer-controller \
    -n kube-system --set clusterName=eksworkshop-eksctl \
    --set serviceAccount.create=false \
    --set serviceAccount.name=aws-load-balancer-controller \
    --set image.tag="${LBC_VERSION}" --set region=${AWS_REGION} \
    --set vpcId=${VPC_ID} --version="${LBC_CHART_VERSION}"

kubectl -n kube-system rollout status deployment aws-load-balancer-controller
```

## Deploying to Fargate
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/main/docs/examples/2048/2048_full.yaml

kubectl -n game-2048 rollout status deployment deployment-2048

kubectl get nodes
```

## Ingress
```bash
kubectl get ingress/ingress-2048 -n game-2048

export FARGATE_GAME_2048=$(kubectl get ingress/ingress-2048 -n game-2048 -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

echo "http://${FARGATE_GAME_2048}"
```

## Cleanup
```bash
kubectl delete -f https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/8c7ce02646a851b55656c7daaa2f053203c87738/docs/examples/2048/2048_full.yaml

helm uninstall aws-load-balancer-controller \
    -n kube-system

eksctl delete iamserviceaccount --cluster eksworkshop-eksctl --name aws-load-balancer-controller \
    --namespace kube-system --wait

aws iam delete-policy \
    --policy-arn arn:aws:iam::${ACCOUNT_ID}:policy/AWSLoadBalancerControllerIAMPolicy

kubectl delete -k "github.com/aws/eks-charts/stable/aws-load-balancer-controller//crds?ref=master"

eksctl delete fargateprofile --name game-2048 --cluster eksworkshop-eksctl
```