resource "aws_dynamodb_table" "dynamodb_table_minute" {
  name = var.table_name_minute
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1
  hash_key = var.partition_key

  attribute {
    name = var.partition_key
    type = "S"
  }
}

resource "aws_dynamodb_table" "dynamodb_table_hour" {
  name = var.table_name_hour
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1
  hash_key = var.partition_key

  attribute {
    name = var.partition_key
    type = "S"
  }
}

resource "aws_dynamodb_table" "dynamodb_table_day" {
  name = var.table_name_day
  billing_mode = "PROVISIONED"
  read_capacity = 1
  write_capacity = 1
  hash_key = var.partition_key

  attribute {
    name = var.partition_key
    type = "S"
  }
}

