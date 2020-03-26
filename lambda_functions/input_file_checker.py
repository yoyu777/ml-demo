import json
import boto3
import datetime

import os


S3_BUCKET_NAME=os.environ['S3_BUCKET_NAME']
REGION=os.environ['REGION']

def run(event,content):
    timestamp=event['timestamp']
    print(timestamp)
    return 