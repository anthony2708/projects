terraform {
  backend "s3" {
    bucket         = "anthony-terraform-bucket"
    key            = "env/dev/web-services/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "anthony-terraform-state-lock"
  }
}