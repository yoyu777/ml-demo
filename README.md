




1) Create an S3 bucket for Terraform state files

```
cd $workspace/terraform/state-bucket
terraform init 
terraform apply 
terraform output -json  > state_bucket_outputs.json
```
Update `base.backend-config` and `service.backend-config` files in `base` and `service` directory accordingly

2) Initialise terrafrom backend in `base` and `service` folders
```
cd $workspace/terraform/base
terraform init -backend-config=base.backend-config 

cd $workspace/terraform/service
terraform init -backend-config=service.backend-config 
```

3) Deploy terraform modules in base folder

Update the values in `terraform.tfvars` if necessary.
```
cd $workspace/terraform/base
terraform apply
terraform output -json  > base_outputs.json

cd $workspace/terraform/service
terraform apply
```

