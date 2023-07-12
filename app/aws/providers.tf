terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.0"
    }

    archive = {
      source  = "hashicorp/archive"
      version = ">= 2.2.0"
    }

    # null = {
    #   source  = "hashicorp/null"
    #   version = ">= 3.1.0"
    # }
  }
  backend "s3" {
    bucket               = "anthony-terraform-bucket"
    dynamodb_table       = "anthony_terraform_state"
    key                  = "app/terraform.tfstate"
    region               = "us-east-1"
    workspace_key_prefix = "tfstate:"
  }
  required_version = "~> 1.4.0"
}

provider "aws" {
  region = var.region
}