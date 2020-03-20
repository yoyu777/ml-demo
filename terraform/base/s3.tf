

resource "aws_s3_bucket" "base_bucket" {
  bucket = "bucket-${var.PROJECT_NAME}-${var.ENVIRONMENT}-${random_id.self.hex}"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

