#!/bin/bash

set -e

# Deploy Windows Server IIS
echo "Creating namespace..."
# TODO: If-else condition
kubectl create namespace windows

echo "Creating Templatefile"
cat << EoF > ~/code/k8s/windows/windows_server_iis.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: windows-server-iis
  namespace: windows
spec:
  selector:
    matchLabels:
      app: windows-server-iis
      tier: backend
      track: stable
  replicas: 1
  template:
    metadata:
      labels:
        app: windows-server-iis
        tier: backend
        track: stable
    spec:
      containers:
      - name: windows-server-iis
        image: mcr.microsoft.com/windows/servercore:ltsc2019-amd64
        ports:
        - name: http
          containerPort: 80
        imagePullPolicy: IfNotPresent
        command:
        - powershell.exe
        - -command
        - "Add-WindowsFeature Web-Server; Invoke-WebRequest -UseBasicParsing -Uri 'https://dotnetbinaries.blob.core.windows.net/servicemonitor/2.0.1.6/ServiceMonitor.exe' -OutFile 'C:\\ServiceMonitor.exe'; echo '<html><body><br/><br/><marquee><H1>Hello EKS!!!<H1><marquee></body><html>' > C:\\inetpub\\wwwroot\\default.html; C:\\ServiceMonitor.exe 'w3svc'; "
      nodeSelector:
        kubernetes.io/os: windows
---
apiVersion: v1
kind: Service
metadata:
  name: windows-server-iis-service
  namespace: windows
spec:
  ports:
  - port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: windows-server-iis
    tier: backend
    track: stable
  sessionAffinity: None
  type: LoadBalancer
EoF

echo "Applying configuration..."
kubectl apply -f ~/code/k8s/windows/windows_server_iis.yaml

echo "Checking resources..."
kubectl -n windows get svc,deploy,pods

echo "Checking the DNS Domain..."
export WINDOWS_IIS_SVC=$(kubectl -n windows get svc -o jsonpath='{.items[].status.loadBalancer.ingress[].hostname}')

echo http://${WINDOWS_IIS_SVC}

