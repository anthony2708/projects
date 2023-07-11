# Configure the AWS provider
provider "aws" {
  region = "us-west-2"
}

# Create a S3 bucket
resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name
  lifecycle {
    prevent_destroy = false
  }

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_state_ver" {
  bucket = aws_s3_bucket.terraform_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

