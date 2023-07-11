#!/bin/bash

set -e

echo "Deleting resources..."
# Optional
calicoctl delete -f - < ~/code/k8s/windows/deny_icmp.yaml
unalias calicoctl
kubectl delete -f https://docs.projectcalico.org/archive/v3.15/manifests/calicoctl.yaml
# Required
kubectl delete -f ~/code/k8s/windows/sample-deployments.yaml
kubectl delete -f ~/code/k8s/windows/user-rolebinding.yaml
kubectl delete -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/master/config/v1.6/calico.yaml
kubectl delete -f ~/code/k8s/windows/windows_server_iis.yaml

kubectl delete namespace windows

eksctl delete nodegroup -f ~/code/k8s/windows/windows_nodes.yaml --approve --wait

rm -rf ~/code/k8s/windows/*.yaml

eksctl delete cluster --name=eksworkshop-eksctl

echo "Done, thank you for using the app!"
echo "Anh Bui - anh.t.bui@opswat.com"
