




1) 

`project_config.cfg` 



```
aws iam create-service-linked-role --aws-service-name ecs.amazonaws.com
```


2)


sh deploy.sh


> AccessDeniedException: Neither the global service principal states.amazonaws.com, nor the regional one is authorized to assume the provided role.


3)

put secrets in 



4)

sh run_task.sh