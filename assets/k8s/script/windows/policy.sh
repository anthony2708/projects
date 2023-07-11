#!/bin/bash

set -e

echo "Creating policy..."
cat << EOF > ~/code/k8s/windows/sample-deployments.yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: nginx-deployment
    namespace: windows
spec:
    selector:
        matchLabels:
            app: nginx
    replicas: 1
    template:
        metadata:
            labels:
                app: nginx
        spec:
            containers:
            - name: nginx
              image: nginx:1.7.9
              securityContext:
                privileged: true
            nodeSelector:
                beta.kubernetes.io/os: linux
EOF

echo "Applying the configuration..."
kubectl apply -f ~/code/k8s/windows/sample-deployments.yaml

echo "Checking the pods..."
kubectl get pods -o wide --watch -n windows
