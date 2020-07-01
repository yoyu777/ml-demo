WORKSPACE=$(pwd)

cd $WORKSPACE

cd $WORKSPACE/base
terraform destroy -auto-approve

cd $WORKSPACE/service
terraform destroy -auto-approve

cd $WORKSPACE
rm state-bucket/outputs.json
rm base/outputs.json
rm service/outputs.json
rm -r base/.terraform/
rm -r service/.terraform/