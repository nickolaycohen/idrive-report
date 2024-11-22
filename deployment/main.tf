# Configure the AWS Provider
provider "aws" {
  region = "us-east-1"
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "archive_file" "lambda" {
  type = "zip"
  source_dir = "${path.module}/../src"
  output_path = "lambda.zip"
}

resource "aws_lambda_function" "lambda" {
  filename = "lambda.zip"
  function_name = "python_terraform_lambda"
  role = aws_iam_role.iam_for_lambda.arn
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime = "python3.10"
  handler = "lambda.lambda_handler"
  timeout = 180
}