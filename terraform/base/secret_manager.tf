resource "aws_secretsmanager_secret" "secret" {
  name_prefix = "secret-${var.PROJECT_NAME}-${var.ENVIRONMENT}-"
}
