variable "bucket_name" {
  description = "Name of the S3 Bucket"
  default     = "anthony-terraform-bucket"
}

variable "statedb_name" {
  description = "Name of the DynamoDB structure"
  default     = "anthony-terraform-state-lock"
}