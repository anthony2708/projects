provider "aws" {
  shared_credentials_files = ["~/.aws/credentials"]
  profile                  = "default"
  region                   = var.region
}

resource "aws_s3_bucket" "statefile" {
  bucket = "anthony-terraform-state"

  lifecycle {
    prevent_destroy = false
  }

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_state_ver" {
  bucket = aws_s3_bucket.statefile.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "lockfile" {
  name           = "terraform_state"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    "Name" = "DynamoDB StateLock Table"
  }
}