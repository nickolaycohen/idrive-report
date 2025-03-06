resource "aws_security_group" "postgres_sg" {
  vpc_id = "vpc-3623974d" #aws_vpc.main.id
  name   = "postgres_sg"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Change to restrict access
  }
}

data "aws_ssm_parameter" "db_username" {
  name  = "/rds/postgres/username"
  with_decryption = true
}

data "aws_ssm_parameter" "db_password" {
  name  = "/rds/postgres/password"
  with_decryption = true
}

resource "aws_db_instance" "postgres" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine              = "postgres"
  engine_version      = "14.17"
  instance_class      = "db.t3.micro"
  identifier         = var.db_identifier
  username          = data.aws_ssm_parameter.db_username.value
  password          = data.aws_ssm_parameter.db_password.value
  publicly_accessible = true
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.postgres_sg.id]
}


data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = ["vpc-3623974d"]  #[aws_vpc.main.id]
  }
}

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = ["subnet-de0924f1","subnet-a57e5df8"]
  tags = {
    Name = "DBSubnetGroups"
  }
}

