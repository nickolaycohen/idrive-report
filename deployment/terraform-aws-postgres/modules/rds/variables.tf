variable "db_identifier" {
  type    = string
  default = "my-postgres-db"
}

variable "db_username" {
  type    = string
  default = "adminuser"
}

variable "db_password" {
  type    = string
  sensitive = true
}