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
      PROJECT_NAME = var.PROJECT_NAME
      ENVIRONMENT = var.ENVIRONMENT
    }
  }

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

resource "aws_lambda_function" "model_selection" {
  filename      = "../../lambda_functions/archive.zip"
  source_code_hash = data.archive_file.lambda_functions.output_base64sha256
  function_name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Model-Selection"
  role          = module.lambda_model_selection_role.arn
  handler       = "model_selection.run"
  runtime       = "python3.8"

  environment {
    variables = {
      S3_BUCKET_NAME = var.S3_BUCKET_NAME
      REGION = var.REGION
      PROJECT_NAME = var.PROJECT_NAME
      ENVIRONMENT = var.ENVIRONMENT
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
    filter_prefix       = "staging/"
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
  policy_arns  = [aws_iam_policy.lambda_object_watcher_role_policy.arn,
                  aws_iam_policy.cloudwatch_logger_role_policy.arn]
}


// Lambda-Input-File-Checker-Role


module "lambda_input_file_checker_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Lambda-Input-File-Checker-Role"
  services     = ["lambda.amazonaws.com"]
  policy_arns  = [aws_iam_policy.s3_data_bucket_role_policy.arn,
                  aws_iam_policy.cloudwatch_logger_role_policy.arn]
}


// Lambda-Model-Selection-Role


module "lambda_model_selection_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Lambda-Model-Selection-Role"
  services     = ["lambda.amazonaws.com"]
  policy_arns  = [aws_iam_policy.state_machine_role_policy.arn,
                  aws_iam_policy.cloudwatch_logger_role_policy.arn]
}
