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
  services     = ["lambda.amazonaws.com"]
  policy_arns  = [aws_iam_policy.state_machine_role_policy.arn]
}

resource "aws_iam_policy" "state_machine_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-State-Machine-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.state_machine_role_policy_document.json}"
}

data "aws_iam_policy_document" "state_machine_role_policy_document" {
  statement {
    sid = "s3"

    actions = [
      "s3:*"
    ]

    resources = [
      "arn:aws:s3:::${var.S3_BUCKET_NAME}",
      "arn:aws:s3:::${var.S3_BUCKET_NAME}/*",
    ]
  }

  statement {
    sid = "logs"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "*"
    ]
  }
}

