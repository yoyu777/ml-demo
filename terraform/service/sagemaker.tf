module "sagemaker_execution_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Sagemaker-Execution-Role"
  services     = ["sagemaker.amazonaws.com"]
  policy_arns  = [aws_iam_policy.s3_data_bucket_role_policy.arn,
                  aws_iam_policy.cloudwatch_logger_role_policy.arn]
}
