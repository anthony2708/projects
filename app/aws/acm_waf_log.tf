# Create a certificate for the webapp
# module "acm_app" {
#   source  = "terraform-aws-modules/acm/aws"
#   version = "~> 4.0"

#   domain_name       = var.webapp_domain
#   validation_method = "DNS"

#   wait_for_validation    = false
#   create_route53_records = false
#   validation_record_fqdns = [
#     "${var.webapp_domain}",
#     "${var.api_domain}",
#   ]

#   subject_alternative_names = [
#     "${var.api_domain}",
#   ]

#   tags = {
#     Name      = "${var.webapp_domain}",
#     Alternate = "${var.api_domain}",
#   }
# }

module "acm_dev" {
  source  = "terraform-aws-modules/acm/aws"
  version = "~> 4.0"

  domain_name       = var.dev_domain
  validation_method = "DNS"

  wait_for_validation    = false
  create_route53_records = false
  validation_record_fqdns = [
    "${var.dev_domain}",
  ]

  subject_alternative_names = [
    "${var.dev_domain}"
  ]

  tags = {
    Name = "${var.dev_domain}",
  }
}

# Create a firewall for the webapp
# TODO: Wait for New version to be released for API Gateway
# which supports the following ACL
resource "aws_wafv2_web_acl" "webapp" {
  name        = "webapp-firewall"
  scope       = "REGIONAL"
  description = "The firewall for the Services Portal"
  # provider    = aws.region

  default_action {
    allow {}
  }

  # Rule 1: Count the number of requests from Vietnam
  rule {
    name     = "RateLimitFromVietnam"
    priority = 1

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 200
        aggregate_key_type = "IP"

        scope_down_statement {
          geo_match_statement {
            country_codes = ["VN"]
          }
        }
      }

    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "VietnamDOS"
      sampled_requests_enabled   = true
    }
  }

  # Rule 2: Count the number of requests from other countries
  rule {
    name     = "RateLimitFromOtherCountries"
    priority = 2

    action {
      block {}
    }

    statement {
      rate_based_statement {
        limit              = 100
        aggregate_key_type = "IP"

        scope_down_statement {
          not_statement {
            statement {
              geo_match_statement {
                country_codes = ["VN"]
              }
            }
          }
        }
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "WorldDOS"
      sampled_requests_enabled   = true
    }
  }

  # Rule 3: General rules
  rule {
    name     = "CommonRule"
    priority = 21

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesCommonRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "CommonRule"
      sampled_requests_enabled   = true
    }
  }

  # Rule 4: Bad Input rules
  rule {
    name     = "BadInputRule"
    priority = 22

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesKnownBadInputsRuleSet"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "BadInputRule"
      sampled_requests_enabled   = true
    }
  }

  # Rule 5: IP Reputation rules
  rule {
    name     = "IPReputationRule"
    priority = 23

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAmazonIpReputationList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "IPReputationRule"
      sampled_requests_enabled   = true
    }
  }

  # Rule 6: Annoymous IP rules
  rule {
    name     = "AnonymousIPRule"
    priority = 24

    override_action {
      none {}
    }

    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesAnonymousIpList"
        vendor_name = "AWS"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "AnonymousIPRule"
      sampled_requests_enabled   = true
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "webapp-firewall"
    sampled_requests_enabled   = true
  }
}

# Create a log group for the webapp
# resource "aws_cloudwatch_log_group" "webapp" {
#   name              = "/aws/lambda/getVideo"
#   retention_in_days = 14
# }

# resource "aws_cloudwatch_log_group" "getUrl" {
#   name              = "/aws/lambda/getUrl"
#   retention_in_days = 14
# }

# resource "aws_cloudwatch_log_group" "postUrl" {
#   name              = "/aws/lambda/postUrl"
#   retention_in_days = 14
# }

# # Create a log group for the api
# resource "aws_cloudwatch_log_group" "webapi" {
#   name              = "/aws/apigateway/lambda_api"
#   retention_in_days = 14
# }