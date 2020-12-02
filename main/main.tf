provider "aws" {
  region = var.aws_region
  profile = var.aws_profile
  version = "2.23.0"
}

module "dynamodb" {
  source = "../modules/dynamodb"
  table_name = var.table_name
  partition_key = var.partition_key
}

