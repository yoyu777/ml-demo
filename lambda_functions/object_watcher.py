from __future__ import print_function
import urllib
import boto3
import json
import os
import re


STATE_MACHINE_ARN=os.environ['STATE_MACHINE_ARN']
REGION=os.environ['REGION']

# event content structure:
# https://docs.aws.amazon.com/AmazonS3/latest/dev/notification-content-structure.html


def run(event,content):
    # intialize required boto3 clients
    step_function = boto3.client('stepfunctions', region_name=REGION)

    #parse the key from lambda event payload
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    print('Found new object %s' % key)

    if m:=re.match(r"staging/\w*-(\d*).csv",key):
        print("Found timestamp: %s" % m.group(1))
        timestamp=m.group(1)

        #get the status of state machine
        sfn_response = step_function.list_executions(
            stateMachineArn = STATE_MACHINE_ARN,
            statusFilter='RUNNING'
        )

        # check the status of state machine
        if(len(sfn_response['executions']) >= 1):
            print('Another job is running. Skip.')
        else:
            sfn_execution_response = step_function.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps({
                    "timestamp":timestamp
                })
            )

            print('Execution ARN: %s' % sfn_execution_response['executionArn'])

            return timestamp

    else:
        raise Exception('Key does not match pattern')