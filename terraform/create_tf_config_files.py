import configparser
import os
import json
from pathlib import Path

cwd=Path(__file__).parent.absolute()

print("cwd: %s" % cwd)
config = configparser.ConfigParser()
config.read(cwd.parent.joinpath('project_config.cfg'))

tf_state_bucket_outputs=json.load(open(cwd.joinpath('state-bucket/outputs.json')))

def write_config_files(layer):
    with open(cwd.joinpath('%s/terraform.tfvars' % layer), 'w') as tfvars:
        tfvars.write('PROJECT_NAME = "%s"\n' % config['main']['PROJECT_NAME'])
        tfvars.write('ENVIRONMENT = "%s"\n' % config.get('main','ENVIRONMENT'))
        tfvars.write('REGION = "%s"\n' % config.get('main','REGION'))

    with open(cwd.joinpath('%s/backend-config.cfg' % layer), 'w') as tfvars:
        tfvars.write('bucket = "%s"\n' % tf_state_bucket_outputs['TF_STATE_BUCKET']['value'])
        tfvars.write('key = "%s/%s.tfstate"\n' % (config.get('main','ENVIRONMENT'),layer))
        tfvars.write('region = "%s"\n' % config.get('main','REGION'))

write_config_files('base')
write_config_files('service')
