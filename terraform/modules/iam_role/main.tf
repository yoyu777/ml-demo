# Lambda role definition
variable "name" {
  type        = string
  description = "the name of the IAM role"
}

variable "services" {
  type        = list(string)
  description = "the services that can assume this role"
}

variable "policy_arns" {
  type        = list(string)
  description = "the ARNs of the IAM policy to be attached to"
}

variable "PROJECT_NAME" {
  type        = string
}

variable "ENVIRONMENT" {
  type        = string
}

resource "aws_iam_role" "this" {
  name = "${var.PROJECT_NAME}-${var.ENVIRONMENT}-${var.name}"

  assume_role_policy = "${data.aws_iam_policy_document.this.json}"

  tags={
    Project     = var.PROJECT_NAME
    Environment = var.ENVIRONMENT
  }
}

data "aws_iam_policy_document" "this" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = var.services
    }
  }
}

resource "aws_iam_role_policy_attachment" "this" {
  count = length(var.policy_arns)
  role       = "${aws_iam_role.this.name}"
  policy_arn = var.policy_arns[count.index]
}

output "arn" {
  value       = aws_iam_role.this.arn
}
