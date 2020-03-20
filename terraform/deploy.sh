WORKSPACE=$(pwd)

cd $WORKSPACE

# Checking if state-bucket/outputs.json exists

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

# Creating terraform.tfvars and backend-config.cfg files for base and service
cd $WORKSPACE
python create_tf_config_files.py

cd $WORKSPACE/base
terraform init -backend-config=backend-config.cfg

cd $WORKSPACE/service
terraform init -backend-config=backend-config.cfg

echo "Done"