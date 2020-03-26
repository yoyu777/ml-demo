output "TASK_ARN" {
  value = aws_ecs_task_definition.data_collector.arn
}

output "GLUE_JOB_NAME" {
  value = aws_glue_job.etl_job.name
}


