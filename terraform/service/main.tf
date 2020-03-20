# Configure the AWS Provider
provider "aws" {
  version = "~> 2.0"
  region  = var.REGION
}

resource "random_id" "bucket_id" {
  byte_length = 8
}