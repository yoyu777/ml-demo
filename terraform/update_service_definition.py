import json
import configparser
import os


from pathlib import Path

from sagemaker.amazon.amazon_estimator import get_image_uri

from create_tf_config_files import write_config_files

write_config_files('service')

cwd=Path(__file__).parent.absolute()

config = configparser.ConfigParser()


config.read(cwd.parent.joinpath('project_config.cfg'))
base_layer_outputs=json.load(open(cwd.joinpath('base/outputs.json')))



S3_BUCKET_NAME=base_layer_outputs['S3_BUCKET_NAME']['value']
S3_BUCKET_ARN=base_layer_outputs['S3_BUCKET_ARN']['value']
GLUE_BUCKET_NAME=base_layer_outputs['GLUE_BUCKET_NAME']['value']

SECRET_ARN=base_layer_outputs['SECRET_ARN']['value']
SECRET_NAME=base_layer_outputs['SECRET_NAME']['value']



if cwd.joinpath('service/outputs.json').exists():   # This script may be run before the creation of service layer
    service_layer_outputs=json.load(open(cwd.joinpath('service/outputs.json')))
else:
    service_layer_outputs={}

if 'SAGEMAKER_EXECUTION_ROLE_ARN' in service_layer_outputs:
    SAGEMAKER_EXECUTION_ROLE_ARN=service_layer_outputs['SAGEMAKER_EXECUTION_ROLE_ARN']['value']
else:
    SAGEMAKER_EXECUTION_ROLE_ARN=''


# Updating service/terraform.tfvars 

with open(cwd.joinpath('service/terraform.tfvars'), 'a') as tfvars:
    tfvars.write('S3_BUCKET_NAME = "%s"\n' % S3_BUCKET_NAME)
    tfvars.write('S3_BUCKET_ARN = "%s"\n' % S3_BUCKET_ARN)
    tfvars.write('SECRET_ARN = "%s"\n' % SECRET_ARN)
    tfvars.write('GLUE_BUCKET_NAME = "%s"\n' % GLUE_BUCKET_NAME)

# Updating ECS Task definition file

definition_template=open(cwd.joinpath('service/template-data-collector-container-definition.json'),'r')
definition=json.load(definition_template)

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

definition_template.close()

json.dump(definition, open(cwd.joinpath('service/data-collector-container-definition.json'),'w'))

# Updating training_job_definition file
training_job_definition_file_path=cwd.joinpath('../sagemaker/training_job_definition.json')
training_job_definition=json.load(open(training_job_definition_file_path,'r'))


training_image = get_image_uri(config.get('main','REGION'), 'linear-learner')
training_job_definition['AlgorithmSpecification']['TrainingImage']=training_image

training_data='s3://{}/transformed/{}'.format(S3_BUCKET_NAME, 'training_data.io')
test_data='s3://{}/transformed/{}'.format(S3_BUCKET_NAME, 'test_data.io')
validation_data='s3://{}/transformed/{}'.format(S3_BUCKET_NAME, 'validation_data.io')

training_job_definition['InputDataConfig'][0]['DataSource']['S3DataSource']['S3Uri']=training_data
training_job_definition['InputDataConfig'][1]['DataSource']['S3DataSource']['S3Uri']=test_data
training_job_definition['InputDataConfig'][2]['DataSource']['S3DataSource']['S3Uri']=validation_data

S3OutputPath='s3://{}/output'.format(S3_BUCKET_NAME)
training_job_definition['OutputDataConfig']['S3OutputPath']=S3OutputPath


training_job_definition['RoleArn']=SAGEMAKER_EXECUTION_ROLE_ARN

json.dump(training_job_definition, open(training_job_definition_file_path,'w'))


# Getting Tuning job config

tuning_job_config_path=cwd.joinpath('../sagemaker/tuning_job_config.json')
tuning_job_config=json.load(open(tuning_job_config_path,'r'))

# Updating State Machine definition file
state_machine_definition_file_path=cwd.joinpath('../step_function/state_machine_definition.json')
state_machine_definition=json.load(open(state_machine_definition_file_path,'r'))

states=state_machine_definition['States']
name_prefix="%s-%s-" % (config.get('main','PROJECT_NAME'),config.get('main','ENVIRONMENT'))

states['Input_File_Checker']['Parameters']['FunctionName']="%sInput-File-Checker" % name_prefix

states['Glue_StartJobRun']['Parameters']['JobName']="%sGlue-ETL-Job" % name_prefix

states['Sagemaker_CreateHyperParameterTuningJob']['Parameters']['HyperParameterTuningJobConfig']=tuning_job_config
states['Sagemaker_CreateHyperParameterTuningJob']['Parameters']['TrainingJobDefinition']=training_job_definition

states['Model_Selection']['Parameters']['FunctionName']="%sModel-Selection" % name_prefix

states['Sagemaker_CreateModel']['Parameters']['ExecutionRoleArn']=SAGEMAKER_EXECUTION_ROLE_ARN

states['Sagemaker_CreateEndpoint']['Parameters']['ExecutionRoleArn']=SAGEMAKER_EXECUTION_ROLE_ARN


json.dump(state_machine_definition, open(state_machine_definition_file_path,'w'))

pass