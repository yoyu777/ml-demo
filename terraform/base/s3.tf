

resource "aws_s3_bucket" "base_bucket" {
  bucket_prefix = "bucket-${var.PROJECT_NAME}-${var.ENVIRONMENT}-"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}


resource "aws_s3_bucket" "glue_bucket" {
  bucket_prefix = "aws-glue-${var.PROJECT_NAME}-${var.ENVIRONMENT}-"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}