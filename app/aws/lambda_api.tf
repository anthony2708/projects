# # API & Lambda for the website
# data "archive_file" "lambdaVideo" {
#   type        = "zip"
#   source_dir  = "api/getVideo"
#   output_path = "api/getVideo.zip"
# }

# data "archive_file" "lambdaUrl" {
#   type        = "zip"
#   source_dir  = "api/getUrl"
#   output_path = "api/getUrl.zip"
# }

# data "archive_file" "lambdaPostUrl" {
#   type        = "zip"
#   source_dir  = "api/postUrl"
#   output_path = "api/postUrl.zip"
# }

# data "archive_file" "lambdaLayers" {
#   type        = "zip"
#   source_dir  = "api/dist"
#   output_path = "api/layers.zip"
# }

# resource "aws_lambda_layer_version" "getVideo" {
#   filename            = data.archive_file.lambdaLayers.output_path
#   layer_name          = "getVideo"
#   source_code_hash    = data.archive_file.lambdaLayers.output_base64sha256
#   compatible_runtimes = ["nodejs18.x"]
# }

# resource "aws_lambda_function" "getVideo" {
#   function_name    = "getVideo"
#   role             = aws_iam_role.lambda_execution.arn
#   handler          = "index.handler"
#   runtime          = "nodejs18.x"
#   filename         = data.archive_file.lambdaVideo.output_path
#   publish          = true
#   timeout          = 10
#   source_code_hash = data.archive_file.lambdaVideo.output_base64sha256
#   layers           = [aws_lambda_layer_version.getVideo.arn]

#   depends_on = [
#     aws_cloudwatch_log_group.webapp,
#     aws_iam_role_policy_attachment.iam,
#     data.archive_file.lambdaVideo,
#     aws_lambda_layer_version.getVideo
#   ]
# }

# resource "aws_lambda_function" "getUrlDev" {
#   function_name    = "getUrl"
#   role             = aws_iam_role.lambda_execution.arn
#   handler          = "index.handler"
#   runtime          = "nodejs18.x"
#   filename         = data.archive_file.lambdaUrl.output_path
#   publish          = true
#   timeout          = 5
#   source_code_hash = data.archive_file.lambdaUrl.output_base64sha256
#   layers           = [aws_lambda_layer_version.getVideo.arn]

#   depends_on = [
#     aws_cloudwatch_log_group.getUrl,
#     aws_iam_role_policy_attachment.iam,
#     data.archive_file.lambdaUrl,
#     aws_lambda_layer_version.getVideo
#   ]

#   environment {
#     variables = {
#       "MY_AWS_ACCESS_KEY_ID"     = var.aws_access_key,
#       "MY_AWS_SECRET_ACCESS_KEY" = var.aws_secret_key,
#       "MY_AWS_REGION"            = var.db_region
#     }
#   }
# }

# resource "aws_lambda_function" "postUrlDev" {
#   function_name    = "postUrl"
#   role             = aws_iam_role.lambda_execution.arn
#   handler          = "index.handler"
#   runtime          = "nodejs18.x"
#   filename         = data.archive_file.lambdaPostUrl.output_path
#   publish          = true
#   timeout          = 5
#   source_code_hash = data.archive_file.lambdaPostUrl.output_base64sha256
#   layers           = [aws_lambda_layer_version.getVideo.arn]

#   depends_on = [
#     aws_cloudwatch_log_group.postUrl,
#     aws_iam_role_policy_attachment.iam,
#     data.archive_file.lambdaPostUrl,
#     aws_lambda_layer_version.getVideo
#   ]

#   environment {
#     variables = {
#       "MY_AWS_ACCESS_KEY_ID"     = var.aws_access_key,
#       "MY_AWS_SECRET_ACCESS_KEY" = var.aws_secret_key,
#       "MY_AWS_REGION"            = var.db_region
#     }
#   }
# }

# resource "aws_apigatewayv2_api" "lambda" {
#   name                         = var.api_name
#   protocol_type                = "HTTP"
#   disable_execute_api_endpoint = true

#   depends_on = [
#     aws_cloudwatch_log_group.webapi
#   ]

#   cors_configuration {
#     allow_origins = ["https://${var.webapp_domain}"]
#     allow_methods = ["GET", "POST", "OPTIONS"]
#     allow_headers = ["content-type"]
#     max_age       = 300
#   }
# }

# resource "aws_apigatewayv2_domain_name" "webapp" {
#   depends_on = [
#     module.acm_app
#   ]

#   domain_name = var.api_domain

#   domain_name_configuration {
#     certificate_arn = module.acm_app.acm_certificate_arn
#     endpoint_type   = "REGIONAL"
#     security_policy = "TLS_1_2"
#   }
# }

# resource "aws_apigatewayv2_api_mapping" "webapp" {
#   api_id      = aws_apigatewayv2_api.lambda.id
#   domain_name = aws_apigatewayv2_domain_name.webapp.domain_name
#   stage       = aws_apigatewayv2_stage.lambda.name
# }

# resource "aws_apigatewayv2_stage" "lambda" {
#   api_id      = aws_apigatewayv2_api.lambda.id
#   name        = var.api_stage
#   auto_deploy = true

#   access_log_settings {
#     destination_arn = aws_cloudwatch_log_group.webapi.arn
#     format = jsonencode({
#       requestId               = "$context.requestId"
#       sourceIp                = "$context.identity.sourceIp"
#       requestTime             = "$context.requestTime"
#       protocol                = "$context.protocol"
#       httpMethod              = "$context.httpMethod"
#       resourcePath            = "$context.resourcePath"
#       routeKey                = "$context.routeKey"
#       status                  = "$context.status"
#       responseLength          = "$context.responseLength"
#       integrationErrorMessage = "$context.integrationErrorMessage"
#     })
#   }

#   route_settings {
#     route_key              = "POST /api/getVideo"
#     throttling_burst_limit = 20
#     throttling_rate_limit  = 20
#   }

#   route_settings {
#     route_key              = "POST /dev"
#     throttling_burst_limit = 5
#     throttling_rate_limit  = 5
#   }

#   route_settings {
#     route_key              = "GET /{id}"
#     throttling_burst_limit = 5
#     throttling_rate_limit  = 5
#   }
# }

# resource "aws_apigatewayv2_integration" "lambda" {
#   api_id = aws_apigatewayv2_api.lambda.id

#   integration_type   = "AWS_PROXY"
#   integration_uri    = aws_lambda_function.getVideo.invoke_arn
#   integration_method = "POST"
# }

# resource "aws_apigatewayv2_integration" "getUrlDev" {
#   api_id = aws_apigatewayv2_api.lambda.id

#   integration_type   = "AWS_PROXY"
#   integration_uri    = aws_lambda_function.getUrlDev.invoke_arn
#   integration_method = "POST"
# }

# resource "aws_apigatewayv2_integration" "postUrlDev" {
#   api_id = aws_apigatewayv2_api.lambda.id

#   integration_type   = "AWS_PROXY"
#   integration_uri    = aws_lambda_function.postUrlDev.invoke_arn
#   integration_method = "POST"
# }

# resource "aws_apigatewayv2_route" "lambda" {
#   api_id    = aws_apigatewayv2_api.lambda.id
#   route_key = "POST /api/getVideo"
#   target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
# }

# resource "aws_apigatewayv2_route" "getUrlDev" {
#   api_id    = aws_apigatewayv2_api.lambda.id
#   route_key = "GET /{id}"
#   target    = "integrations/${aws_apigatewayv2_integration.getUrlDev.id}"
# }

# resource "aws_apigatewayv2_route" "postUrlDev" {
#   api_id    = aws_apigatewayv2_api.lambda.id
#   route_key = "POST /dev"
#   target    = "integrations/${aws_apigatewayv2_integration.postUrlDev.id}"
# }
