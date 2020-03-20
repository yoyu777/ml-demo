
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name ="vpc-${var.PROJECT_NAME}-${var.ENVIRONMENT}"
  cidr = "10.0.0.0/16"

  azs             = ["eu-west-2b"]
  public_subnets  = ["10.0.101.0/24"]

  enable_nat_gateway = false

  tags = {
    Module      = "terraform-aws-modules/vpc/aws"
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

resource "aws_ecs_cluster" "ecs_cluster" {
  name = "ecs-cluster-${var.PROJECT_NAME}-${var.ENVIRONMENT}"
  capacity_providers = ["FARGATE"]

  default_capacity_provider_strategy  {
      capacity_provider = "FARGATE"
  }

  setting{
    name = "containerInsights"
    value="enabled"
  }

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}
