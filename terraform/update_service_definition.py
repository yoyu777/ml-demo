import json
import configparser
import os
from pathlib import Path

cwd=Path(__file__).parent.absolute()

config = configparser.ConfigParser()
config.read(cwd.parent.joinpath('project_config.cfg'))

# Updating service/terraform.tfvars 
base_layer_outputs=json.load(open(cwd.joinpath('base/outputs.json')))

S3_BUCKET_NAME=base_layer_outputs['S3_BUCKET_NAME']['value']
SECRET_ARN=base_layer_outputs['SECRET_ARN']['value']
SECRET_NAME=base_layer_outputs['SECRET_NAME']['value']


with open(cwd.joinpath('service/terraform.tfvars'), 'a') as tfvars:
    tfvars.write('S3_BUCKET_NAME = "%s"\n' % S3_BUCKET_NAME)
    tfvars.write('SECRET_ARN = "%s"\n' % SECRET_ARN)

# Updating ECS Task definition file

definition_file=open(cwd.joinpath('service/data-collector-container-definition.json'),'r')
definition=json.load(definition_file)

definition[0]["name"]="%s-%s" %(config.get('main','PROJECT_NAME'),config.get('main','ENVIRONMENT'))

definition[0]["environment"].append({
    "name": "LOGLEVEL",
    "value": config.get('main','LOGLEVEL')
})

definition[0]["environment"].append({
    "name": "REGION",
    "value": config.get('main','REGION')
})

definition[0]["environment"].append({
    "name": "S3_BUCKET_NAME",
    "value": S3_BUCKET_NAME
})

definition[0]["environment"].append({
    "name": "SECRET_NAME",
    "value": SECRET_NAME
})

definition[0]["LogConfiguration"]["Options"]["awslogs-region"]=config.get('main','REGION')
definition[0]["LogConfiguration"]["Options"]["awslogs-group"]='/ecs/%s' % definition[0]["name"]

definition_file.close()

with open(cwd.joinpath('service/data-collector-container-definition.json'),'w') as definition_file:
    json.dump(definition, definition_file)


pass