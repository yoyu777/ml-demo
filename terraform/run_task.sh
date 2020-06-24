aws ecs run-task \
--cluster $(cd base && terraform output ECS_CLUSTER_ARN) \
--count 1 \
--launch-type FARGATE \
--platform-version LATEST \
--task-definition $(cd service && terraform output TASK_ARN) \
--network-configuration "awsvpcConfiguration={subnets=[$(cd base && terraform output -json PUBLIC_SUBNETS | jq '.[0]')],assignPublicIp=ENABLED}"
