mkdir python_libs
cp *.py python_libs/
cd python_libs
zip python_libs.zip *
aws s3 cp python_libs.zip s3://ml-lab-pyspark/ --profile ml-lab
cd ..
