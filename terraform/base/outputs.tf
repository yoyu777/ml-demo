output "S3_BUCKET_NAME" {
  value = aws_s3_bucket.base_bucket.bucket
}

output "SECRET_NAME"{
    value=aws_secretsmanager_secret.secret.name
}