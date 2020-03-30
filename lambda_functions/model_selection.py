import os

PROJECT_NAME=os.environ['PROJECT_NAME']
ENVIRONMENT=os.environ['ENVIRONMENT']

def run(event,context):
    print(event)
    if 'HyperParameterTuningJobStatus' in event and event['HyperParameterTuningJobStatus']=='Completed':
        best_job_name=event["BestTrainingJob"]["TrainingJobName"]
        output_path=event["TrainingJobDefinition"]["OutputDataConfig"]["S3OutputPath"]
        image=event["TrainingJobDefinition"]["AlgorithmSpecification"]["TrainingImage"]

        return {
            "model_name":best_job_name,
            "image":image,
            "model_data_url":'%s/%s/output/model.tar.gz' % (output_path,best_job_name),
            "endpoint_identifier":'%s-%s' % (PROJECT_NAME,ENVIRONMENT)
        }

    else:
        raise Exception('HyperParameterTuningJobStatus not completed')