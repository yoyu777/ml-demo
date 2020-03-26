terraform {
  required_version = "~> 0.12"
}

# Configure the AWS Provider
provider "aws" {
  version = "~> 2.0"
  region  = var.REGION
}

variable "PROJECT_NAME" {
    default="mldemo"
}

variable "ENVIRONMENT" {
    default="dev"
}

variable "REGION" {
    default="eu-west-2"
}

resource "aws_s3_bucket" "state_bucket" {
  bucket_prefix = "tf-state-bucket-${var.PROJECT_NAME}-"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

output "TF_STATE_BUCKET" {
  value = aws_s3_bucket.state_bucket.bucket
}