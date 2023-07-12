# # IAM role for Lambda functions to access dynamoDB & API Gateway
# resource "aws_iam_role" "lambda_execution" {
#   name = "lambda_execution"
#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Action = "sts:AssumeRole"
#         Principal = {
#           Service = "lambda.amazonaws.com"
#         }
#         Effect = "Allow"
#         Sid    = ""
#       }
#     ]
#   })
# }

# resource "aws_iam_policy" "iam_policy" {
#   name        = "iam_policy"
#   description = "IAM policy for lambda function"
#   path        = "/"
#   policy = jsonencode({
#     Version = "2012-10-17",
#     Statement = [
#       {
#         Effect = "Allow"
#         Action = [
#           "logs:CreateLogGroup",
#           "logs:CreateLogStream",
#           "logs:PutLogEvents"
#         ],
#         Resource = ["arn:aws:logs:*:*:*"],
#       }
#   ] })
# }

# resource "aws_iam_role_policy_attachment" "iam" {
#   role       = aws_iam_role.lambda_execution.name
#   policy_arn = aws_iam_policy.iam_policy.arn
# }

# resource "aws_lambda_permission" "api" {
#   statement_id  = "AllowExecutionFromAPIGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.getVideo.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_stage.lambda.execution_arn}/POST/api/${aws_lambda_function.getVideo.function_name}"
# }

# resource "aws_lambda_permission" "getDev" {
#   statement_id  = "AllowExecutionFromAPIGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.getUrlDev.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_stage.lambda.execution_arn}/GET/{id}"
# }

# resource "aws_lambda_permission" "postDev" {
#   statement_id  = "AllowExecutionFromAPIGateway"
#   action        = "lambda:InvokeFunction"
#   function_name = aws_lambda_function.postUrlDev.function_name
#   principal     = "apigateway.amazonaws.com"

#   source_arn = "${aws_apigatewayv2_stage.lambda.execution_arn}/POST/dev"
# }

resource "aws_iam_role_policy" "lambda_policy" {
  name = "dynamodb_lambda_policy"
  role = aws_iam_role.lambda_execution.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ],
        Resource = ["arn:aws:dynamodb:ap-southeast-1:165777862211:table/${var.db_url}"]
      }
    ]
  })
}

# resource "aws_iam_policy" "access_s3" {
#   name = "AccessS3"
#   policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Action = [
#           "s3:PutObject",
#           "s3:PutObjectAcl",
#           "s3:ListBucket"
#         ]
#         Resource = [
#           "${aws_s3_bucket.static_webapp.arn}/*"
#         ]
#       }
#     ]
#   })
# }

resource "aws_iam_policy" "access_dev_s3" {
  name = "AccessDevS3"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:PutObjectAcl",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.dev_webapp.arn}/*"
        ]
      }
    ]
  })
}

# IAM role for CloudFront to access S3 bucket

# resource "aws_s3_bucket_policy" "webapp" {
#   bucket = aws_s3_bucket.static_webapp.id
#   policy = data.aws_iam_policy_document.react_app_s3.json
# }

resource "aws_s3_bucket_policy" "dev_webapp" {
  bucket = aws_s3_bucket.dev_webapp.id
  policy = data.aws_iam_policy_document.dev_app_s3.json
}