resource "aws_ecs_task_definition" "data_collector" {
  family                   = "ml-demo"
  container_definitions    = "${file("data-collector-container-definition.json")}"
  task_role_arn            = aws_iam_role.task_role.arn
  execution_role_arn       = aws_iam_role.task_role.arn
  network_mode             = "awsvpc" # Required by Fargate
  cpu                      = 256
  memory                   = 512
  requires_compatibilities = ["FARGATE"]
  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

resource "aws_cloudwatch_log_group" "data_collector" {
  name = "/ecs/${var.PROJECT_NAME}-${var.ENVIRONMENT}"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

# Task role definition

resource "aws_iam_role" "task_role" {
  name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-ECS-Task-Role"

  assume_role_policy = "${data.aws_iam_policy_document.task_role_assume_role_policy.json}"

  tags = {
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

data "aws_iam_policy_document" "task_role_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_policy" "task_role_policy" {
  name   = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-ECS-Task-Role-Policy"
  path   = "/"
  policy = "${data.aws_iam_policy_document.task_role_policy_document.json}"
}

data "aws_iam_policy_document" "task_role_policy_document" {
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
    sid = "secretsmanager"

    actions = [
      "secretsmanager:GetSecretValue"
    ]

    resources = [
      "${var.SECRET_ARN}"
    ]
  }


  statement {
    sid = "logs"

    actions = [
      "logs:*"
    ]

    resources = [
      "${aws_cloudwatch_log_group.data_collector.arn}",
      "${aws_cloudwatch_log_group.data_collector.arn}:*"
    ]
  }
}

resource "aws_iam_role_policy_attachment" "task_role_policy_attachment" {
  role       = "${aws_iam_role.task_role.name}"
  policy_arn = "${aws_iam_policy.task_role_policy.arn}"
}

