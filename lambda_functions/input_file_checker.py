import json
import boto3
import datetime

import os


S3_BUCKET_NAME=os.environ['S3_BUCKET_NAME']
REGION=os.environ['REGION']
PROJECT_NAME=os.environ['PROJECT_NAME']
ENVIRONMENT=os.environ['ENVIRONMENT']

boto3.setup_default_session(region_name=REGION)

class InsufficientKeys(Exception):
    pass

def run(event,content):
    print(json.dumps(event))
    timestamp=event['Input']['timestamp']
    print(timestamp)

    key_list = [
       'staging/deals-%s.csv' % timestamp,
       'staging/price-%s.csv' % timestamp
    ]

    keys_found=[]
    
    for key in key_list:
        client = boto3.client('s3')
        response = client.list_objects(
            Bucket=S3_BUCKET_NAME,
            Prefix=key
        )
        
        if 'Contents' in response and len(response['Contents'])>0:
            keys_found.append(key)
        else:
            break
    
    response_message='Expecting %s keys, found %s' % (len(key_list),len(keys_found))

    print(response_message)

    if len(key_list)==len(keys_found):
        return {
            "deals":'deals-%s.csv' % timestamp,
            "price":'price-%s.csv' % timestamp,
            "identifier":'%s-%s-%s' % (PROJECT_NAME,ENVIRONMENT,timestamp)
        }
    else:
        raise InsufficientKeys(response_message)