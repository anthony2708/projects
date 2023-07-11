# Configure the AWS provider
provider "aws" {
  region = "us-west-2"

}

# Create an IAM user
resource "aws_iam_user" "example" {
  count = length(var.user_names)
  name  = element(var.user_names, count.index)

}

# Data source: IAM policy document
data "aws_iam_policy_document" "ec2_read_only" {
  statement {
    effect    = "Allow"
    actions   = ["ec2:Describe*"]
    resources = ["*"]
  }
}

# Create an IAM policy
resource "aws_iam_policy" "ec2_read_only" {
  name   = "ec2-read-only"
  policy = data.aws_iam_policy_document.ec2_read_only.json
}

# Create an IAM user policy attachement
resource "aws_iam_user_policy_attachment" "ec2_access" {
  count      = length(var.user_names)
  user       = element(aws_iam_user.example.*.name, count.index)
  policy_arn = aws_iam_policy.ec2_read_only.arn
}
