aws s3 cp ../glue/glue-etl.py s3://$(cd base && terraform output GLUE_BUCKET_NAME)/
aws s3 cp ../glue/glue_dependencies-0.1-py3-none-any.whl s3://$(cd base && terraform output GLUE_BUCKET_NAME)/
