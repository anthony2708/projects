provider "aws" {
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "default"
  region                   = var.region
}

terraform {
  backend "s3" {
    bucket         = "anthony-terraform-state"
    key            = "test/terraform.tfstate"
    encrypt        = true
    region         = "us-west-2"
    dynamodb_table = "terraform_state"
  }
}
