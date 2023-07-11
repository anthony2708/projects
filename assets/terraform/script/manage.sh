#!/bin/bash
set -e

echo "Creating new folder..."
mkdir ~/code/terraform/learn-terraform-deploy-nginx-kubernetes
cd ~/code/terraform/learn-terraform-deploy-nginx-kubernetes

echo "Creating tfConfig file..."
touch kubernetes.tf
cat <<EoF > kubernetes.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.20.0"
    }

    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.0.1"
    }
  }
}

data "terraform_remote_state" "eks" {
  backend = "local"

  config = {
    path = "../learn-terraform-provision-eks-cluster/terraform.tfstate"
  }
}

# Retrieve EKS cluster information
provider "aws" {
  region = data.terraform_remote_state.eks.outputs.region
}

data "aws_eks_cluster" "cluster" {
  name = data.terraform_remote_state.eks.outputs.cluster_id
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
  exec {
    api_version = "client.authentication.k8s.io/v1alpha1"
    command     = "aws"
    args = [
      "eks",
      "get-token",
      "--cluster-name",
      data.aws_eks_cluster.cluster.name
    ]
  }
}

resource "kubernetes_deployment" "nginx" {
  metadata {
    name = "scalable-nginx-example"
    labels = {
      App = "ScalableNginxExample"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        App = "ScalableNginxExample"
      }
    }
    template {
      metadata {
        labels = {
          App = "ScalableNginxExample"
        }
      }
      spec {
        container {
          image = "nginx:1.7.8"
          name  = "example"

          port {
            container_port = 80
          }

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "nginx" {
  metadata {
    name = "nginx-example"
  }
  spec {
    selector = {
      App = kubernetes_deployment.nginx.spec.0.template.0.metadata[0].labels.App
    }
    port {
      port        = 80
      target_port = 80
    }

    type = "LoadBalancer"
  }
}

output "lb_ip" {
  value = kubernetes_service.nginx.status.0.load_balancer.0.ingress.0.hostname
}

EoF

echo "Initializing..."
terraform init

echo "Checking and Validating..."
terraform fmt
terraform validate
terraform plan
terraform apply

echo "Kubernetes created, checking..."
kubectl get deployments
kubectl get services

echo "Destroying..."
terraform destroy

echo "Creating crontab"
touch crontab_crd.tf
cat <<EoF > crontab_crd.tf
resource "kubernetes_manifest" "crontab_crd" {
  manifest = {
    "apiVersion" = "apiextensions.k8s.io/v1"
    "kind"       = "CustomResourceDefinition"
    "metadata" = {
      "name" = "crontabs.stable.example.com"
    }
    "spec" = {
      "group" = "stable.example.com"
      "names" = {
        "kind"   = "CronTab"
        "plural" = "crontabs"
        "shortNames" = [
          "ct",
        ]
        "singular" = "crontab"
      }
      "scope" = "Namespaced"
      "versions" = [
        {
          "name" = "v1"
          "schema" = {
            "openAPIV3Schema" = {
              "properties" = {
                "spec" = {
                  "properties" = {
                    "cronSpec" = {
                      "type" = "string"
                    }
                    "image" = {
                      "type" = "string"
                    }
                  }
                  "type" = "object"
                }
              }
              "type" = "object"
            }
          }
          "served"  = true
          "storage" = true
        },
      ]
    }
  }
}
EoF

echo "Creating custom resources..."
touch my_new_crontab.tf
cat << EoF > my_new_crontab.tf
resource "kubernetes_manifest" "my_new_crontab" {
  manifest = {
    "apiVersion" = "stable.example.com/v1"
    "kind"       = "CronTab"
    "metadata" = {
      "name"      = "my-new-cron-object"
      "namespace" = "default"
    }
    "spec" = {
      "cronSpec" = "* * * * */5"
      "image"    = "my-awesome-cron-image"
    }
  }
}
EoF

echo "Reapplying..."
terraform apply

echo "Checking crons..."
kubectl get crds

echo "Checking definition..."
kubectl get crontabs
kubectl describe crontab my-new-cron-object

echo "Destroying..."
terraform destroy
