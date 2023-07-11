terraform {
  backend "s3" {
    bucket         = "anthony-terraform-bucket"
    key            = "env/prod/mysql/terraform.tfstate"
    region         = "us-west-2"
    dynamodb_table = "anthony-terraform-state-lock"
    encrypt        = true
  }
}