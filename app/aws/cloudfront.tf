# module "webapp" {
#   source = "terraform-aws-modules/cloudfront/aws"

#   depends_on = [
#     aws_s3_bucket.static_webapp,
#     module.acm_app,
#     # aws_wafv2_web_acl.webapp
#   ]

#   aliases = ["${var.webapp_domain}"]

#   enabled                       = true
#   is_ipv6_enabled               = true
#   price_class                   = "PriceClass_200"
#   retain_on_delete              = false
#   wait_for_deployment           = false
#   default_root_object           = "index.html"
#   create_origin_access_identity = true
#   origin_access_identities = {
#     bucket = aws_s3_bucket.static_webapp.id
#   }

#   origin = {
#     api = {
#       domain_name = var.api_domain
#       custom_origin_config = {
#         http_port              = 80
#         https_port             = 443
#         origin_protocol_policy = "match-viewer"
#         origin_ssl_protocols   = ["TLSv1", "TLSv1.1", "TLSv1.2"]
#       }

#       custom_header = [
#         {
#           name  = "X-Forwarded-Scheme"
#           value = "https"
#         },
#         {
#           name  = "X-Frame-Options"
#           value = "SAMEORIGIN"
#         }
#       ]
#     }

#     "services.builetuananh.name.vn" = {
#       domain_name = aws_s3_bucket.static_webapp.bucket_regional_domain_name
#       s3_origin_config = {
#         origin_access_identity = "bucket"
#       }
#     }
#   }

#   default_cache_behavior = {
#     target_origin_id       = "services.builetuananh.name.vn"
#     allowed_methods        = ["GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "DELETE"]
#     cached_methods         = ["GET", "HEAD", "OPTIONS"]
#     viewer_protocol_policy = "redirect-to-https"
#     min_ttl                = 3600
#     default_ttl            = 5400
#     max_ttl                = 7200
#     compress               = true
#     query_string           = false
#   }

#   ordered_cache_behavior = [
#     {
#       path_pattern           = "/index.html"
#       target_origin_id       = "services.builetuananh.name.vn"
#       allowed_methods        = ["GET", "HEAD", "OPTIONS"]
#       cached_methods         = ["GET", "HEAD"]
#       viewer_protocol_policy = "redirect-to-https"
#       min_ttl                = 3600
#       default_ttl            = 5400
#       max_ttl                = 7200
#       compress               = true
#       query_string           = false
#       }, {
#       target_origin_id       = "services.builetuananh.name.vn"
#       path_pattern           = "/youtube.html"
#       allowed_methods        = ["GET", "HEAD", "OPTIONS"]
#       cached_methods         = ["GET", "HEAD"]
#       viewer_protocol_policy = "redirect-to-https"
#       # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
#       min_ttl      = 3600
#       default_ttl  = 5400
#       max_ttl      = 7200
#       compress     = true
#       query_string = false
#       }, {
#       target_origin_id       = "services.builetuananh.name.vn"
#       path_pattern           = "/url.html"
#       allowed_methods        = ["GET", "HEAD", "OPTIONS"]
#       cached_methods         = ["GET", "HEAD"]
#       viewer_protocol_policy = "redirect-to-https"
#       # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
#       min_ttl      = 3600
#       default_ttl  = 5400
#       max_ttl      = 7200
#       compress     = true
#       query_string = false
#       }, {
#       target_origin_id       = "services.builetuananh.name.vn"
#       path_pattern           = "/assets/*"
#       allowed_methods        = ["GET", "HEAD", "OPTIONS"]
#       cached_methods         = ["GET", "HEAD"]
#       viewer_protocol_policy = "redirect-to-https"
#       # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
#       min_ttl      = 3600
#       default_ttl  = 5400
#       max_ttl      = 7200
#       compress     = true
#       query_string = false
#       }, {
#       target_origin_id       = "services.builetuananh.name.vn"
#       path_pattern           = "/img/*"
#       allowed_methods        = ["GET", "HEAD", "OPTIONS"]
#       cached_methods         = ["GET", "HEAD"]
#       viewer_protocol_policy = "redirect-to-https"
#       # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
#       min_ttl      = 3600
#       default_ttl  = 5400
#       max_ttl      = 7200
#       compress     = true
#       query_string = false
#     }
#   ]

#   custom_error_response = [{
#     error_caching_min_ttl = 300
#     error_code            = 404
#     response_code         = 404
#     response_page_path    = "/404.html"
#     }, {
#     error_caching_min_ttl = 300
#     error_code            = 403
#     response_code         = 200
#     response_page_path    = "/404.html"
#   }]

#   geo_restriction = {
#     restriction_type = "whitelist"
#     locations        = ["VN"]
#   }

#   viewer_certificate = {
#     acm_certificate_arn      = module.acm_app.acm_certificate_arn
#     ssl_support_method       = "sni-only"
#     minimum_protocol_version = "TLSv1.2_2019"
#   }

#   # web_acl_id = aws_wafv2_web_acl.webapp.arn
# }

module "dev_webapp" {
  source = "terraform-aws-modules/cloudfront/aws"

  depends_on = [
    aws_s3_bucket.dev_webapp,
    module.acm_dev,
    # aws_wafv2_web_acl.webapp
    aws_cloudfront_function.redirect
  ]

  aliases = ["${var.dev_domain}"]

  enabled                       = true
  is_ipv6_enabled               = true
  price_class                   = "PriceClass_200"
  retain_on_delete              = false
  wait_for_deployment           = false
  default_root_object           = "index.html"
  create_origin_access_identity = true
  origin_access_identities = {
    bucket = aws_s3_bucket.dev_webapp.id
  }

  origin = {

    "dev.builetuananh.name.vn" = {
      domain_name = aws_s3_bucket.dev_webapp.bucket_regional_domain_name
      s3_origin_config = {
        origin_access_identity = "bucket"
      }
    }
  }

  default_cache_behavior = {
    target_origin_id       = "dev.builetuananh.name.vn"
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT", "DELETE"]
    cached_methods         = ["GET", "HEAD", "OPTIONS"]
    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 3600
    default_ttl            = 5400
    max_ttl                = 7200
    compress               = true
    query_string           = false
  }

  ordered_cache_behavior = [
    {
      target_origin_id       = "dev.builetuananh.name.vn"
      path_pattern           = "/index.html"
      allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      cached_methods         = ["GET", "HEAD"]
      viewer_protocol_policy = "redirect-to-https"
      min_ttl                = 3600
      default_ttl            = 5400
      max_ttl                = 7200
      compress               = true
      query_string           = false
      }, 
      # {
      # target_origin_id       = "dev.builetuananh.name.vn"
      # path_pattern           = "/games"
      # allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      # cached_methods         = ["GET", "HEAD"]
      # viewer_protocol_policy = "redirect-to-https"
      # min_ttl                = 3600
      # default_ttl            = 5400
      # max_ttl                = 7200
      # compress               = true
      # query_string           = false

      # function_association = {
      #   viewer-request = {
      #     function_arn = aws_cloudfront_function.redirect.arn
      #   }
      # } }, {
      # target_origin_id       = "dev.builetuananh.name.vn"
      # path_pattern           = "/games/*"
      # allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      # cached_methods         = ["GET", "HEAD"]
      # viewer_protocol_policy = "redirect-to-https"
      # min_ttl                = 3600
      # default_ttl            = 5400
      # max_ttl                = 7200
      # compress               = true
      # query_string           = false

      # function_association = {
      #   viewer-request = {
      #     function_arn = aws_cloudfront_function.redirect.arn
      #   }
      # }
      # }, 
      {
      target_origin_id       = "dev.builetuananh.name.vn"
      path_pattern           = "/gallery"
      allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      cached_methods         = ["GET", "HEAD"]
      viewer_protocol_policy = "redirect-to-https"
      min_ttl                = 3600
      default_ttl            = 5400
      max_ttl                = 7200
      compress               = true
      query_string           = false

      function_association = {
        viewer-request = {
          function_arn = aws_cloudfront_function.redirect.arn
        }
      } }, {
      target_origin_id       = "dev.builetuananh.name.vn"
      path_pattern           = "/gallery/*"
      allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      cached_methods         = ["GET", "HEAD"]
      viewer_protocol_policy = "redirect-to-https"
      min_ttl                = 3600
      default_ttl            = 5400
      max_ttl                = 7200
      compress               = true
      query_string           = false

      function_association = {
        viewer-request = {
          function_arn = aws_cloudfront_function.redirect.arn
        }
      }
      }, {
      target_origin_id       = "dev.builetuananh.name.vn"
      path_pattern           = "/public/*"
      allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      cached_methods         = ["GET", "HEAD"]
      viewer_protocol_policy = "redirect-to-https"
      # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
      min_ttl      = 3600
      default_ttl  = 5400
      max_ttl      = 7200
      compress     = true
      query_string = false
    }, {
      target_origin_id       = "dev.builetuananh.name.vn"
      path_pattern           = "/gallery/public/*"
      allowed_methods        = ["GET", "HEAD", "OPTIONS"]
      cached_methods         = ["GET", "HEAD"]
      viewer_protocol_policy = "redirect-to-https"
      # response_headers_policy_id = "67f7725c-6f97-4210-82d7-5512b31e9d03"
      min_ttl      = 3600
      default_ttl  = 5400
      max_ttl      = 7200
      compress     = true
      query_string = false
    }
  ]

  custom_error_response = [{
    error_caching_min_ttl = 300
    error_code            = 404
    response_code         = 404
    response_page_path    = "/404.html"
    }, {
    error_caching_min_ttl = 300
    error_code            = 403
    response_code         = 200
    response_page_path    = "/404.html"
  }]

  geo_restriction = {
    restriction_type = "whitelist"
    locations        = ["VN"]
  }

  viewer_certificate = {
    acm_certificate_arn      = module.acm_dev.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = "TLSv1.2_2019"
  }

  # web_acl_id = aws_wafv2_web_acl.webapp.arn
}

resource "aws_cloudfront_function" "redirect" {
  name    = "RedirectURL"
  runtime = "cloudfront-js-1.0"
  code    = file("api/redirect/index.js")
}