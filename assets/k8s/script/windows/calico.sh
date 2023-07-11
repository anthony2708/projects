#!/bin/bash

# Optional
set -e
echo "Deploying Calico on the Cluster..."
kubectl apply -f https://raw.githubusercontent.com/aws/amazon-vpc-cni-k8s/release-1.6/config/v1.6/calico.yaml

echo "Checking for daemonset..."
kubectl get daemonset calico-node --namespace=kube-system

echo "Creating RoleBinding"
cat << EOF > ~/code/k8s/windows/user-rolebinding.yaml
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: nodes-cluster-admin
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: Group
  name: system:nodes
EOF

echo "Applying RoleBinding"
kubectl apply -f ~/code/k8s/windows/user-rolebinding.yaml

echo "Applying CalicoCTL"
kubectl apply -f https://docs.projectcalico.org/archive/v3.15/manifests/calicoctl.yaml 
alias calicoctl="kubectl exec -i -n kube-system calicoctl -- /calicoctl"

cat << EOF > ~/code/k8s/windows/deny_icmp.yaml
---
kind: GlobalNetworkPolicy
apiVersion: projectcalico.org/v3
metadata:
    name: block-icmp
spec:
  order: 200
  selector: all()
  types:
  - Ingress
  - Egress
  ingress:
  - action: Deny
    protocol: ICMP
  - action: Deny
    protocol: ICMPv6
  egress:
  - action: Deny
    protocol: ICMP
  - action: Deny
    protocol: ICMPv6
EOF

calicoctl apply -f - < ~/code/k8s/windows/deny_icmp.yaml
