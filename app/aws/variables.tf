data "aws_availability_zones" "available" {}
# data "aws_iam_policy_document" "react_app_s3" {
#   depends_on = [
#     module.webapp
#   ]

#   statement {
#     actions = ["s3:GetObject"]
#     resources = [
#       aws_s3_bucket.static_webapp.arn,
#       "${aws_s3_bucket.static_webapp.arn}/*"
#     ]
#     principals {
#       type        = "AWS"
#       identifiers = module.webapp.cloudfront_origin_access_identity_iam_arns
#     }
#   }
# }

data "aws_iam_policy_document" "dev_app_s3" {
  depends_on = [
    module.dev_webapp
  ]

  statement {
    actions = ["s3:GetObject"]
    resources = [
      aws_s3_bucket.dev_webapp.arn,
      "${aws_s3_bucket.dev_webapp.arn}/*"
    ]
    principals {
      type        = "AWS"
      identifiers = module.dev_webapp.cloudfront_origin_access_identity_iam_arns
    }
  }
}

variable "aws_access_key" {}
variable "aws_secret_key" {
  sensitive = true
}
variable "region" {
  description = "The region of the application (need for migrating to different regions)"
  default     = "us-east-1"
}

variable "app_name" {
  description = "The name of the application"
  default     = "anthony-services-portal"
}

variable "cidr" {
  description = "The network of the application"
  default     = "10.0.0.0/16"
}

variable "bucket_name" {
  description = "The name of the S3 backend bucket"
  default     = "anthony_terraform_bucket"
}

# variable "webapp_bucket" {
#   description = "The name of the S3 web bucket"
#   default     = "services.builetuananh.name.vn"
# }

variable "dev_webapp_bucket" {
  description = "The name of the S3 dev bucket"
  default     = "dev.builetuananh.name.vn"
}

# variable "webapp_domain" {
#   description = "The domain of the webapp"
#   default     = "services.builetuananh.name.vn"
# }

# variable "api_domain" {
#   description = "The domain of the api"
#   default     = "api.builetuananh.name.vn"
# }

variable "dev_domain" {
  description = "The domain of the dev VM"
  default     = "dev.builetuananh.name.vn"
}

variable "db_table" {
  description = "The name of the AWS DynamoDB table"
  default     = "anthony_terraform_state"
}

variable "db_url" {
  description = "The AWS DynamoDB for URL Shortener"
  default     = "URLShortener"
}

variable "db_region" {
  description = "The region of the AWS DynamoDB"
  default     = "ap-southeast-1"
}

# variable "api_name" {
#   description = "The name of the API"
#   default     = "lambda_api"
# }

# variable "api_stage" {
#   description = "The stage of the API"
#   default     = "lambda_stage"
# }

variable "vm_ami" {
  description = "The AMI of the machine"
  default     = "ami-082b1f4237bd816a1"
}

locals {
  mime_types = {
    ".html" = "text/html"
    ".css"  = "text/css"
    ".js"   = "application/javascript"
    ".ico"  = "image/vnd.microsoft.icon"
    ".jpeg" = "image/jpeg"
    ".jpg"  = "image/jpeg"
    ".png"  = "image/png"
    ".svg"  = "image/svg+xml"
    "CNAME" = "text/plain"
    ".json" = "application/json"
    ".txt"  = "text/plain"
    ".map"  = "application/json"
  }
}