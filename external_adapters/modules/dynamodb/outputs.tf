output "table_name_min" {
  value = aws_dynamodb_table.dynamodb_table_minute.id
}

output "table_arn_min" {
  value = aws_dynamodb_table.dynamodb_table_minute.arn
}

output "table_name_hour" {
  value = aws_dynamodb_table.dynamodb_table_hour.id
}

output "table_arn_hour" {
  value = aws_dynamodb_table.dynamodb_table_hour.arn
}

output "table_name_day" {
  value = aws_dynamodb_table.dynamodb_table_day.id
}

output "table_arn_day" {
  value = aws_dynamodb_table.dynamodb_table_day.arn
}
