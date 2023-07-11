resource "aws_s3_bucket" "terraform_state" {
  bucket = var.bucket_name
  lifecycle {
    prevent_destroy = false
  }

  force_destroy = true
}

resource "aws_s3_bucket_versioning" "terraform_version" {
  bucket = var.bucket_name
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_lock" {
  name           = var.db_table
  hash_key       = "LockID"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "LockID"
    type = "S"
  }
}