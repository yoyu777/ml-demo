WORKSPACE=$(pwd)

cd $WORKSPACE

cd $WORKSPACE/base
terraform destroy -auto-approve

cd $WORKSPACE/service
terraform destroy -auto-approve