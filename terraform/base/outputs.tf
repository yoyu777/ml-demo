output "S3_BUCKET_NAME" {
  value = aws_s3_bucket.base_bucket.bucket
}

output "SECRET_ARN" {
    value=aws_secretsmanager_secret.secret.arn
}

output "SECRET_NAME" {
    value=aws_secretsmanager_secret.secret.name
}

output "ECS_CLUSTER_ARN"{
    value=aws_ecs_cluster.ecs_cluster.arn
}

output "PUBLIC_SUBNETS"{
    value=module.vpc.public_subnets
}