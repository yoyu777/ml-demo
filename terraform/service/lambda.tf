data "archive_file" "lambda_functions" {
  type        = "zip"
  source_dir = "../../lambda_functions"
  output_path = "../../lambda_functions/archive.zip"
}

data "aws_caller_identity" "current" {}

resource "aws_lambda_function" "object_watcher" {
  filename      = "../../lambda_functions/archive.zip"
  source_code_hash = data.archive_file.lambda_functions.output_base64sha256
  function_name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-S3-Object-Watcher"
  role          = module.lambda_object_watcher_role.arn
  handler       = "object_watcher.run"
  runtime       = "python3.8"

  environment {
    variables = {
      STATE_MACHINE_ARN = aws_sfn_state_machine.sfn_state_machine.id
      REGION = var.REGION
    }
  }


  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

resource "aws_lambda_function" "input_file_checker" {
  filename      = "../../lambda_functions/archive.zip"
  source_code_hash = data.archive_file.lambda_functions.output_base64sha256
  function_name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Input-File-Checker"
  role          = module.lambda_input_file_checker_role.arn
  handler       = "input_file_checker.run"
  runtime       = "python3.8"

  environment {
    variables = {
      S3_BUCKET_NAME = var.S3_BUCKET_NAME
      REGION = var.REGION
    }
  }

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

# s3_bucket_notification for object watcher

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.object_watcher.arn}"
  principal     = "s3.amazonaws.com"
  source_arn    = var.S3_BUCKET_ARN
  source_account= data.aws_caller_identity.current.account_id
  // source_account is required
}


resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = var.S3_BUCKET_NAME

  lambda_function {
    lambda_function_arn = "${aws_lambda_function.object_watcher.arn}"
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}

# Lambda-Object-Watcher-Role

module "lambda_object_watcher_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Lambda-Object-Watcher-Role"
  services     = ["lambda.amazonaws.com"]
  policy_arns  = [aws_iam_policy.lambda_object_watcher_role_policy.arn]
}

resource "aws_iam_policy" "lambda_object_watcher_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Lambda-Object-Watcher-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.lambda_object_watcher_role_policy_document.json}"
}

data "aws_iam_policy_document" "lambda_object_watcher_role_policy_document" {
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

  statement {
    sid = "stepfunction"

    actions = [
      "states:*"
    ]

    resources = [
      aws_sfn_state_machine.sfn_state_machine.id
    ]
  }

}

// Lambda-Input-File-Checker-Role


module "lambda_input_file_checker_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Lambda-Input-File-Checker-Role"
  services     = ["lambda.amazonaws.com"]
  policy_arns  = [aws_iam_policy.lambda_input_file_checker_role_policy.arn]
}

resource "aws_iam_policy" "lambda_input_file_checker_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Lambda-Input-File-Checker-Custom-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.lambda_input_file_checker_role_policy_document.json}"
}

data "aws_iam_policy_document" "lambda_input_file_checker_role_policy_document" {
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
