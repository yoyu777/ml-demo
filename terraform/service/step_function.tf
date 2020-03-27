resource "aws_sfn_state_machine" "sfn_state_machine" {
  name       = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-state-machine"
  role_arn   = module.state_machine_role.arn
  definition = file("../../step_function/state_machine_definition.json")


  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

module "state_machine_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "State-Machine-Role"
  services     = ["states.amazonaws.com"]
  policy_arns  = [aws_iam_policy.state_machine_role_policy.arn,
                  aws_iam_policy.s3_data_bucket_role_policy.arn,
                  aws_iam_policy.cloudwatch_logger_role_policy.arn]
}



