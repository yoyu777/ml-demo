resource "aws_secretsmanager_secret" "secret" {
  name = "secret-${var.PROJECT_NAME}-${var.ENVIRONMENT}-${random_id.self.hex}"
}