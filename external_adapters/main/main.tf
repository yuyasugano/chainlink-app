provider "aws" {
  region = var.aws_region
  profile = var.aws_profile
  version = "2.23.0"
}

module "dynamodb" {
  source = "../modules/dynamodb"
  table_name_minute = var.table_name_minute
  table_name_hour = var.table_name_hour
  table_name_day = var.table_name_day
  partition_key = var.partition_key
}

