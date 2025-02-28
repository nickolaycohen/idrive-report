provider "aws" {
  region = "us-east-1"
}

module "rds" {
  source        = "./modules/rds"
  db_identifier = "free-tier-db"
  db_username   = "adminuser"
  db_password   = "mypassword123" # Change this & use AWS Secrets Manager in production
}