resource "aws_glue_job" "etl_job" {
  name     = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Glue-ETL-Job"
  role_arn = "${aws_iam_role.glue_job_role.arn}"

  command {
    name            = "pythonshell"
    script_location = "s3://${var.GLUE_BUCKET_NAME}/glue-etl.py"
    python_version  = "3"
  }
  max_capacity = "0.0625"
  glue_version = "1.0"

  default_arguments = {
    "--S3_BUCKET"                        = var.S3_BUCKET_NAME
    "--extra-py-files"                   = "s3://${var.GLUE_BUCKET_NAME}/glue_dependencies-0.1-py3-none-any.whl"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-continuous-log-filter"     = "true"
    "--continuous-log-logGroup  "        = aws_cloudwatch_log_group.glue_etl.name
  }

  execution_property {
    max_concurrent_runs = 1

  }

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }

}

resource "aws_cloudwatch_log_group" "glue_etl" {
  name = "/aws-glue/etl/${var.PROJECT_NAME}-${var.ENVIRONMENT}"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

# Glue job role definition

resource "aws_iam_role" "glue_job_role" {
  name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Glue-Job-Role"

  assume_role_policy = "${data.aws_iam_policy_document.glue_job_role_assume_role_policy.json}"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

data "aws_iam_policy_document" "glue_job_role_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

resource "aws_iam_role_policy_attachment" "glue_job_role_policy_attachment" {
  role       = "${aws_iam_role.glue_job_role.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}
