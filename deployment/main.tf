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
resource "aws_iam_role" "iam_for_postgres" {
  name = "iam_for_postgres"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::517681850714:root"
        }
        Action = "sts:AssumeRole"
        Condition = {
          StringLike = {
            "aws:PrincipalArn" = "arn:aws:sts::517681850714:assumed-role/AWSReservedSSO_AdministratorAccess_*"
          }
        }
      }
    ]
  })
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

module "rds" {
  source        = "./modules/rds"
  db_identifier = "free-tier-db"
  db_username   = "adminuser"
  db_password   = "mypassword123" # Change this & use AWS Secrets Manager in production
}