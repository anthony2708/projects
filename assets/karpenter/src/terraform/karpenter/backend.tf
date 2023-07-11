terraform {
  backend "s3" {
    bucket               = "anthony-terraform-bucket"
    dynamodb_table       = "anthony-terraform-state-lock"
    key                  = "eks/terraform.tfstate"
    region               = "us-west-2"
    workspace_key_prefix = "tfstate:"
  }
}
