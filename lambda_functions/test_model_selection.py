from model_selection import run
event={
  "HyperParameterTuningJobName": "mldemo-dev-15853298627792",
  "HyperParameterTuningJobArn": "arn:aws:sagemaker:eu-west-2:814948925568:hyper-parameter-tuning-job/mldemo-dev-15853298627792",
  "HyperParameterTuningJobConfig": {
    "Strategy": "Bayesian",
    "HyperParameterTuningJobObjective": {
      "Type": "Maximize",
      "MetricName": "test:binary_f_beta"
    },
    "ResourceLimits": {
      "MaxNumberOfTrainingJobs": 2,
      "MaxParallelTrainingJobs": 2
    },
    "ParameterRanges": {
      "IntegerParameterRanges": [
        {
          "Name": "mini_batch_size",
          "MinValue": "100",
          "MaxValue": "1000"
        }
      ],
      "ContinuousParameterRanges": [
        {
          "Name": "l1",
          "MinValue": "0.0000001",
          "MaxValue": "1"
        },
        {
          "Name": "learning_rate",
          "MinValue": "0.00001",
          "MaxValue": "1"
        },
        {
          "Name": "positive_example_weight_mult",
          "MinValue": "0.00001",
          "MaxValue": "10000"
        },
        {
          "Name": "wd",
          "MinValue": "0.0000001",
          "MaxValue": "1"
        }
      ],
      "CategoricalParameterRanges": [
        {
          "Name": "use_bias",
          "Values": [
            "true",
            "false"
          ]
        }
      ]
    }
  },
  "TrainingJobDefinition": {
    "StaticHyperParameters": {
      "feature_dim": "605",
      "predictor_type": "binary_classifier",
      "_tuning_objective_metric": "test:binary_f_beta",
      "normalize_label": "false",
      "epochs": "15",
      "normalize_data": "true",
      "target_recall": "0.25",
      "binary_classifier_model_selection_criteria": "precision_at_target_recall"
    },
    "AlgorithmSpecification": {
      "TrainingImage": "644912444149.dkr.ecr.eu-west-2.amazonaws.com/linear-learner:1",
      "TrainingInputMode": "File",
      "MetricDefinitions": [
        {
          "Name": "test:dcg",
          "Regex": "#quality_metric: host=\\S+, test dcg <score>=(\\S+)"
        },
        {
          "Name": "train:progress",
          "Regex": "#progress_metric: host=\\S+, completed (\\S+) %"
        },
        {
          "Name": "test:binary_f_beta",
          "Regex": "#quality_metric: host=\\S+, test binary_f_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "train:objective_loss",
          "Regex": "#quality_metric: host=\\S+, epoch=\\S+, train \\S+_objective <loss>=(\\S+)"
        },
        {
          "Name": "validation:macro_precision",
          "Regex": "#quality_metric: host=\\S+, validation macro_precision <score>=(\\S+)"
        },
        {
          "Name": "validation:dcg",
          "Regex": "#quality_metric: host=\\S+, validation dcg <score>=(\\S+)"
        },
        {
          "Name": "test:mse",
          "Regex": "#quality_metric: host=\\S+, test mse <loss>=(\\S+)"
        },
        {
          "Name": "validation:binary_f_beta",
          "Regex": "#quality_metric: host=\\S+, validation binary_f_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "validation:objective_loss",
          "Regex": "#quality_metric: host=\\S+, epoch=\\S+, validation \\S+_objective <loss>=(\\S+)"
        },
        {
          "Name": "validation:objective_loss:final",
          "Regex": "#quality_metric: host=\\S+, validation \\S+_objective <loss>=(\\S+)"
        },
        {
          "Name": "test:macro_recall",
          "Regex": "#quality_metric: host=\\S+, test macro_recall <score>=(\\S+)"
        },
        {
          "Name": "test:absolute_loss",
          "Regex": "#quality_metric: host=\\S+, test absolute_loss <loss>=(\\S+)"
        },
        {
          "Name": "train:recall",
          "Regex": "#quality_metric: host=\\S+, train recall <score>=(\\S+)"
        },
        {
          "Name": "train:mse",
          "Regex": "#quality_metric: host=\\S+, train mse <loss>=(\\S+)"
        },
        {
          "Name": "train:precision",
          "Regex": "#quality_metric: host=\\S+, train precision <score>=(\\S+)"
        },
        {
          "Name": "train:objective_loss:final",
          "Regex": "#quality_metric: host=\\S+, train \\S+_objective <loss>=(\\S+)"
        },
        {
          "Name": "validation:recall",
          "Regex": "#quality_metric: host=\\S+, validation recall <score>=(\\S+)"
        },
        {
          "Name": "test:multiclass_accuracy",
          "Regex": "#quality_metric: host=\\S+, test multiclass_accuracy <score>=(\\S+)"
        },
        {
          "Name": "validation:precision",
          "Regex": "#quality_metric: host=\\S+, validation precision <score>=(\\S+)"
        },
        {
          "Name": "validation:multiclass_accuracy",
          "Regex": "#quality_metric: host=\\S+, validation multiclass_accuracy <score>=(\\S+)"
        },
        {
          "Name": "train:binary_f_beta",
          "Regex": "#quality_metric: host=\\S+, train binary_f_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "test:recall",
          "Regex": "#quality_metric: host=\\S+, test recall <score>=(\\S+)"
        },
        {
          "Name": "test:macro_precision",
          "Regex": "#quality_metric: host=\\S+, test macro_precision <score>=(\\S+)"
        },
        {
          "Name": "test:macro_f_beta",
          "Regex": "#quality_metric: host=\\S+, test macro_f_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "test:objective_loss",
          "Regex": "#quality_metric: host=\\S+, test \\S+_objective <loss>=(\\S+)"
        },
        {
          "Name": "test:precision",
          "Regex": "#quality_metric: host=\\S+, test precision <score>=(\\S+)"
        },
        {
          "Name": "validation:multiclass_top_k_accuracy",
          "Regex": "#quality_metric: host=\\S+, validation multiclass_top_k_accuracy_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "train:binary_classification_accuracy",
          "Regex": "#quality_metric: host=\\S+, train binary_classification_accuracy <score>=(\\S+)"
        },
        {
          "Name": "validation:mse",
          "Regex": "#quality_metric: host=\\S+, validation mse <loss>=(\\S+)"
        },
        {
          "Name": "test:multiclass_top_k_accuracy",
          "Regex": "#quality_metric: host=\\S+, test multiclass_top_k_accuracy_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "validation:binary_classification_accuracy",
          "Regex": "#quality_metric: host=\\S+, validation binary_classification_accuracy <score>=(\\S+)"
        },
        {
          "Name": "train:absolute_loss",
          "Regex": "#quality_metric: host=\\S+, train absolute_loss <loss>=(\\S+)"
        },
        {
          "Name": "validation:macro_recall",
          "Regex": "#quality_metric: host=\\S+, validation macro_recall <score>=(\\S+)"
        },
        {
          "Name": "train:throughput",
          "Regex": "#throughput_metric: host=\\S+, train throughput=(\\S+) records/second"
        },
        {
          "Name": "test:binary_classification_accuracy",
          "Regex": "#quality_metric: host=\\S+, test binary_classification_accuracy <score>=(\\S+)"
        },
        {
          "Name": "validation:absolute_loss",
          "Regex": "#quality_metric: host=\\S+, validation absolute_loss <loss>=(\\S+)"
        },
        {
          "Name": "validation:macro_f_beta",
          "Regex": "#quality_metric: host=\\S+, validation macro_f_\\S+ <score>=(\\S+)"
        },
        {
          "Name": "ObjectiveMetric",
          "Regex": "#quality_metric: host=\\S+, test binary_f_\\S+ <score>=(\\S+)"
        }
      ]
    },
    "RoleArn": "arn:aws:iam::814948925568:role/mldemo-dev-Sagemaker-Execution-Role",
    "InputDataConfig": [
      {
        "ChannelName": "train",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "s3://bucket-mldemo-dev-20200327141354666900000003/training_data.io",
            "S3DataDistributionType": "FullyReplicated"
          }
        },
        "CompressionType": "None"
      },
      {
        "ChannelName": "test",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "s3://bucket-mldemo-dev-20200327141354666900000003/test_data.io",
            "S3DataDistributionType": "FullyReplicated"
          }
        },
        "CompressionType": "None"
      },
      {
        "ChannelName": "validation",
        "DataSource": {
          "S3DataSource": {
            "S3DataType": "S3Prefix",
            "S3Uri": "s3://bucket-mldemo-dev-20200327141354666900000003/validation_data.io",
            "S3DataDistributionType": "FullyReplicated"
          }
        },
        "CompressionType": "None"
      }
    ],
    "OutputDataConfig": {
      "S3OutputPath": "s3://bucket-mldemo-dev-20200327141354666900000003/output"
    },
    "ResourceConfig": {
      "InstanceType": "ml.c4.xlarge",
      "InstanceCount": 1,
      "VolumeSizeInGB": 10
    },
    "StoppingCondition": {
      "MaxRuntimeInSeconds": 43200
    }
  },
  "HyperParameterTuningJobStatus": "Completed",
  "CreationTime": 1585397644473,
  "HyperParameterTuningEndTime": 1585397840494,
  "LastModifiedTime": 1585397840494,
  "BestTrainingJob": {
    "TrainingJobName": "mldemo-dev-15853298627792-001-0f0444b1"
  },
  "Tags": {
    "AWS_STEP_FUNCTIONS_EXECUTION_ARN": "arn:aws:states:eu-west-2:814948925568:execution:mldemo-dev-state-machine:e3ad9152-d75a-49e8-994f-8d625c4337c9",
    "MANAGED_BY_AWS": "STARTED_BY_STEP_FUNCTIONS"
  }
}


result=run(event,None)

pass
