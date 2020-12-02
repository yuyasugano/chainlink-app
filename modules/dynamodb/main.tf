resource "aws_dynamodb_table" "dynamodb-table" {
  name = var.table_name
  billing_mode = "PROVISIONED"
  read_capacity = 3
  write_capacity = 3
  hash_key = var.partition_key

  attribute {
    name = var.partition_key
    type = "S"
  }
}
