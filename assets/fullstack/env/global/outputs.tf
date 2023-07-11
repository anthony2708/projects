output "s3_arn" {
  value = aws_s3_bucket.terraform_state.arn
}

output "dynamodb_arn" {
  value = aws_dynamodb_table.lock.arn
}