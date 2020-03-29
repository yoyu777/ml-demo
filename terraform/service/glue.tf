resource "aws_glue_job" "etl_job" {
  name     = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Glue-ETL-Job"
  role_arn = module.glue_job_role.arn

  command {
    name            = "pythonshell"
    script_location = "s3://${var.GLUE_BUCKET_NAME}/glue-etl.py"
    python_version  = "3"
  }
  max_capacity = "1"
  glue_version = "1.0"
  timeout = "30"

  default_arguments = {
    "--JOB_NAME"                           = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-Glue-ETL"
    "--S3_BUCKET"                        = var.S3_BUCKET_NAME
    "--extra-py-files"                   = "s3://${var.GLUE_BUCKET_NAME}/glue_dependencies-0.1-py3-none-any.whl"
    "--enable-metrics"                   = ""   # Value not needed
    # "--enable-continuous-cloudwatch-log" = "true"
    # "--enable-continuous-log-filter"     = "false"
    # "--continuous-log-logGroup  "        = aws_cloudwatch_log_group.glue_etl.name
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
module "glue_job_role" {
  source = "../modules/iam_role"

  PROJECT_NAME = var.PROJECT_NAME
  ENVIRONMENT  = var.ENVIRONMENT
  name         = "Glue-Job-Role"
  services     = ["glue.amazonaws.com"]
  policy_arns  = ["arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole",
                  aws_iam_policy.s3_data_bucket_role_policy.arn]
}
