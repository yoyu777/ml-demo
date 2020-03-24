WORKSPACE=$(pwd)

cd $WORKSPACE

echo "Checking if state-bucket/outputs.json exists"

if [ -f "state-bucket/outputs.json" ]; then
    echo "State bucekt outputs.json exists. Using state-bucket/outputs.json"
else 
    # If not, deploy Terraform remote state bucket
    echo "State bucekt outputs.json does not exist. Creating Terraform state bucket..."
    cd $WORKSPACE/state-bucket
    terraform init
    terraform apply -auto-approve
    terraform output -json  > outputs.json
fi

echo "Creating terraform.tfvars and backend-config.cfg files for base and service"
cd $WORKSPACE
python create_tf_config_files.py

echo "Initialising base and service layers"
cd $WORKSPACE/base
terraform init -backend-config=backend-config.cfg

cd $WORKSPACE/service
terraform init -backend-config=backend-config.cfg

echo "Deploying the base layer"
cd $WORKSPACE/base
terraform apply -auto-approve
terraform output -json  > outputs.json

echo "Updating service layer definitions"
cd $WORKSPACE
python update_service_definition.py

echo "Deploying the service layer"
cd $WORKSPACE/service
terraform apply -auto-approve
terraform output -json  > outputs.json

echo "Done"