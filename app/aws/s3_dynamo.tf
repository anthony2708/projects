# Bucket for the website
# resource "aws_s3_bucket" "static_webapp" {
#   bucket = var.webapp_bucket
#   tags = {
#     Name = "${var.webapp_bucket}"
#   }
#   lifecycle {
#     prevent_destroy = false
#   }

#   force_destroy = true
# }

resource "aws_s3_bucket" "dev_webapp" {
  bucket = var.dev_webapp_bucket

  tags = {
    Name = "${var.dev_webapp_bucket}"
  }
  lifecycle {
    prevent_destroy = false
  }

  force_destroy = true
}

# resource "aws_s3_bucket_acl" "static_webapp" {
#   bucket = var.webapp_bucket
#   acl    = "private"
# }

resource "aws_s3_bucket_acl" "dev_webapp" {
  bucket = var.dev_webapp_bucket
  acl    = "private"
}

# resource "aws_s3_object" "webapp" {
#   depends_on = [
#     aws_s3_bucket_versioning.static_webapp
#   ]

#   # Run yarn build before applying this, 
#   # and make sure this configuration is run 
#   # on the local machine
#   for_each     = fileset("./client/build", "**/*")
#   bucket       = aws_s3_bucket.static_webapp.bucket
#   key          = each.value
#   source       = "./client/build/${each.value}"
#   etag         = filemd5("./client/build/${each.value}")
#   content_type = lookup(local.mime_types, regex("\\.[^.]+$", each.value), null)
# }

# resource "aws_s3_object" "games" {
#   depends_on = [
#     aws_s3_bucket_versioning.dev_webapp
#   ]

#   # Run yarn build before applying this, 
#   # and make sure this configuration is run 
#   # on the local machine
#   for_each     = fileset("./dev/games/build", "**/*")
#   bucket       = aws_s3_bucket.dev_webapp.bucket
#   key          = "games/${each.value}"
#   source       = "./dev/games/build/${each.value}"
#   etag         = filemd5("./dev/games/build/${each.value}")
#   content_type = lookup(local.mime_types, regex("\\.[^.]+$", each.value), null)
# }

resource "aws_s3_object" "gallery" {
  depends_on = [
    aws_s3_bucket_versioning.dev_webapp
  ]

  # Run yarn build before applying this, 
  # and make sure this configuration is run 
  # on the local machine
  for_each     = fileset("./dev/gallery", "**/*")
  bucket       = aws_s3_bucket.dev_webapp.bucket
  key          = "gallery/${each.value}"
  source       = "./dev/gallery/${each.value}"
  etag         = filemd5("./dev/gallery/${each.value}")
  content_type = lookup(local.mime_types, regex("\\.[^.]+$", each.value), null)
}

resource "aws_s3_object" "intro" {
  depends_on = [
    aws_s3_bucket_versioning.dev_webapp
  ]

  # Run yarn build before applying this, 
  # and make sure this configuration is run 
  # on the local machine
  for_each     = fileset("./dev/intro", "**/*")
  bucket       = aws_s3_bucket.dev_webapp.bucket
  key          = each.value
  source       = "./dev/intro/${each.value}"
  etag         = filemd5("./dev/intro/${each.value}")
  content_type = lookup(local.mime_types, regex("\\.[^.]+$", each.value), null)
}

# resource "aws_s3_bucket_versioning" "static_webapp" {
#   bucket = var.webapp_bucket
#   versioning_configuration {
#     status = "Enabled"
#   }
# }

resource "aws_s3_bucket_versioning" "dev_webapp" {
  bucket = var.dev_webapp_bucket
  versioning_configuration {
    status = "Enabled"
  }
}

# resource "aws_s3_bucket_public_access_block" "public_access_web" {
#   bucket                  = aws_s3_bucket.static_webapp.id
#   block_public_acls       = true
#   block_public_policy     = true
#   ignore_public_acls      = true
#   restrict_public_buckets = true
# }

resource "aws_s3_bucket_public_access_block" "public_access_dev" {
  bucket                  = aws_s3_bucket.dev_webapp.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# resource "aws_s3_bucket_website_configuration" "webapp" {
#   bucket = var.webapp_bucket
#   index_document {
#     suffix = "index.html"
#   }
#   error_document {
#     key = "404.html"
#   }
# }

resource "aws_s3_bucket_website_configuration" "dev" {
  bucket = var.dev_webapp_bucket
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "404.html"
  }
}

resource "aws_dynamodb_table" "dbtable" {
  name           = var.db_url
  hash_key       = "shortURL"
  range_key      = "longURL"
  billing_mode   = "PROVISIONED"
  read_capacity  = 5
  write_capacity = 5

  attribute {
    name = "shortURL"
    type = "S"
  }

  attribute {
    name = "longURL"
    type = "S"
  }
}