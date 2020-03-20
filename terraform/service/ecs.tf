resource "aws_ecs_task_definition" "data_collector" {
  family = "ml-demo"
  container_definitions = "${file("data-collector-container-definition.json")}"
  task_role_arn = aws_iam_role.container_role.arn
  network_mode = "awsvpc" # Required by Fargate
  cpu = 256
  memory = 512
  requires_compatibilities = ["FARGATE"]
  tags={
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}


resource "aws_iam_role" "container_role" {
  name = "${var.PROJECT_NAME}-ECS-Container-Role"

  assume_role_policy = "${data.aws_iam_policy_document.container_role_policy.json}"

  tags={
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

data "aws_iam_policy_document" "container_role_policy" {
  statement {
    sid = "1"

    actions = [
      "s3:*"
    ]

    resources = [
      "arn:aws:s3:::${var.S3_BUCKET_NAME}",
      "arn:aws:s3:::${var.S3_BUCKET_NAME}/*",
    ]
  }

  statement {
    sid = "2"

    actions = [
      "secretsmanager:GetSecretValue"
    ]

    resources = [
      "arn:aws:secretsmanager:${var.REGION}::secret:${var.SECRET_NAME}"    
    ]
  }
}