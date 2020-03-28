// S3-Data-Bucket-Custom-Policy
resource "aws_iam_policy" "s3_data_bucket_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-S3-Data-Bucket-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.s3_data_bucket_role_policy_document.json}"
}

data "aws_iam_policy_document" "s3_data_bucket_role_policy_document" {
  statement {
    sid = "s3"

    actions = [
      "s3:*"
    ]

    resources = ["arn:aws:s3:::${var.S3_BUCKET_NAME}",
      "arn:aws:s3:::${var.S3_BUCKET_NAME}/*"]
  }
}

// CloudWatch-Logger-Custom-Policy
resource "aws_iam_policy" "cloudwatch_logger_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-CloudWatch-Logger-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.cloudwatch_logger_role_policy_document.json}"
}

data "aws_iam_policy_document" "cloudwatch_logger_role_policy_document" {
  statement {
    sid = "logs"

    actions = [
      "cloudwatch:PutMetricData",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
      "logs:CreateLogGroup",
      "logs:DescribeLogStreams"
    ]

    resources = [
      "*"
    ]
  }
}

// Customer Policy for State Machine
resource "aws_iam_policy" "state_machine_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-State-Machine-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.state_machine_role_policy_document.json}"
}

data "aws_iam_policy_document" "state_machine_role_policy_document" {
  statement {
    sid = "lambda"

    actions = [
      "lambda:*"
    ]

    resources = [
      "arn:aws:lambda:${var.REGION}:${data.aws_caller_identity.current.account_id}:function:${var.PROJECT_NAME}-${var.ENVIRONMENT}-*"
    ]
  }

  statement {
    sid = "glue"

    actions = [
      "glue:*"
    ]

    resources = [
      "arn:aws:glue:${var.REGION}:${data.aws_caller_identity.current.account_id}:job/${var.PROJECT_NAME}-${var.ENVIRONMENT}-*"
    ]
  }

   statement {
    sid = "sagemaker"

    actions = [
      "sagemaker:*"
    ]

    resources = [
      "*"
    ]
  }

  statement {
    sid = "passingRoleToSagemaker"

    actions = [
      "iam:PassRole"
    ]

    resources = [
      module.sagemaker_execution_role.arn
    ]

    condition {
      test     = "StringEquals"
      variable = "iam:PassedToService"

      values = [
        "sagemaker.amazonaws.com"
      ]
    }
  }

  statement {
    sid = "cloudwatchmanagedrule"

    actions = [
      "events:PutTargets",
      "events:PutRule",
      "events:DescribeRule"
    ]

    resources = [
     "arn:aws:events:${var.REGION}:${data.aws_caller_identity.current.account_id}:rule/*"
    ]
  }
  
}