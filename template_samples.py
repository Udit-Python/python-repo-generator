template_params = {
    'Parameters': {
        'Environment': {'Type': 'String', 'Default': 'devl', 'Description': 'Environment'},
        'SecurityGroupId': {'Type': 'String', 'Default': 'sg-XXXX', 'Description': 'Security Group for Lambda'},
        'VpcSubnetIds': {'Type': 'String', 'Default': 'subnet-XXXX', 'Description': 'Cloud VPC Subnets for Lambda'},
        'LambdaRoleARN': {'Type': 'String', 'Default': 'aws::::::', 'Description': 'Role for lambda execution'},
        'FunctionName': {'Type': 'String', 'Description': 'Name Of the Lambda'},
        'ComponentName': {'Type': 'String', 'Default': 'default-tag', 'Description': 'Component for tagging'},
        'LayerName': {'Type': 'String', 'Default': 'default-name', 'Description': 'Name Of Layer'},
    }
}

template_resources = {
    'Resources': {
        'LambdaFunction': {
            'Type': 'AWS::Serverless::Function',
            'Properties': {
                'FunctionName': {'Ref': 'FunctionName'},
                'Handler': 'function.lambdafunction.lambda_handler',
                'Runtime': 'python3.8',
                'CodeUri': 'python_function/.',
                'Description': 'Call the AWS Lambda API',
                'Timeout': 120,
                'Environment': {'Variables': {'environment': {'Ref': 'Environment'}}},
                'Role': {"Ref": "LambdaRoleARN"},
                'Tracing': 'Active',
                'VpcConfig': {'SecurityGroupIds': [{'Ref': 'SecurityGroupId'}],
                              'SubnetIds': {"Fn::Split": [',', {"Ref": "VpcSubnetIds"}]}},
                'Layers': [{'Ref': 'libs'}],
                'Tags': {'component': {'Ref': 'ComponentName'}}
            }
        },
        'libs': {
            'Type': 'AWS::Serverless::LayerVersion',
            'Properties': {
                'LayerName': {'Ref': 'LayerName'},
                'Description': 'Dependencies for the blank-python sample app.',
                'ContentUri': 'package/.',
                'CompatibleRuntimes': ['python3.8']
            }
        },
        "LambdaFunctionLogGroup": {
            "Type": "AWS::Logs::LogGroup",
            "Properties": {
                "LogGroupName": {
                    "Fn::Join": ["", ["/aws/lambda/", {"Ref": "FunctionName"}, ]]
                },
                "RetentionInDays": 30,
                "Tags": [
                    {
                        "Key": "component",
                        "Value": {
                            "Ref": "ComponentName"
                        }
                    }
                ]
            },
            "DependsOn": "LambdaFunction"
        },
    }
}

template_resources_kibana = {
    "params": {
        'KibanaRole': {'Type': 'String', 'Default': 'default-role', 'Description': 'ARN of firehose for kibana loging'},
        'KibanaStreamName': {'Type': 'String', 'Default': 'ocdt-vpn-kfh148', 'Description': 'Kibana stream '},
        'KFHLogExtensionArn': {
            'Type': 'AWS::SSM::Parameter::Value<String>', 'Default': 'KFH-LOG-EXTENSION-ARN',
            'Description': 'ARN of Kinesis Firehose KFHLogExtensionArn. '
        },
    },
    "lambda_env": {
        "CROSS_ACCOUNT_ROLE_ARN_TO_BE_ASSUMED": {
            "Ref": "KibanaRole"
        },
        "KFH_STREAM_NAME": {
            "Ref": "KibanaStreamName"
        }
    },
    "layer": {'Ref': 'KFHLogExtensionArn'}
}

template_resources_alarms = {
    "params": {
        'TeamEmailTopic': {'Type': 'String', 'Default': 'default-topic', 'Description': 'Email Alert in Failure'},
        'CustomMetricName': {
            'Type': 'String', 'Default': 'defaultMetricName', 'Description': 'Custom Metrics For Errors'
        },
        'CustomMetricNamespace': {
            'Type': 'String', 'Default': 'defaultMetricNameSpace',
            'Description': 'Custom Metrics Name Space for Custom Metrics'
        },
        'ServiceNowTopicArn': {'Type': 'String', 'Description': 'Service Now Topic Low ARN'},
        'ServiceNowTopicArnHigh': {'Type': 'String', 'Description': 'Service Now Topic High ARN'},
        'CIName': {'Type': 'String', 'Description': 'Service Now CI Name'},
    },
    "resources": {
        "CustomMetricFilter": {
            "Type": "AWS::Logs::MetricFilter",
            "Properties": {
                "FilterPattern": '"[ERROR]"',
                'LogGroupName': {
                    'Ref': 'LambdaFunctionLogGroup'
                },
                'MetricTransformations': [
                    {
                        "MetricValue": 1,
                        "MetricName": {
                            "Ref": "CustomMetricName"
                        },
                        "MetricNamespace": {
                            "Ref": "CustomMetricNamespace"
                        }
                    }
                ],

            }
        },
        "LambdaErrorAlert": {
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": {
                    "Fn::Join": [
                        "-",
                        [
                            {
                                "Ref": "FunctionName"
                            },
                            "alarm"
                        ]
                    ]
                },
                "AlarmDescription": {
                    "Ref": "CIName"
                },
                "MetricName": {
                    "Ref": "CustomMetricName"
                },
                "Namespace": {
                    "Ref": "CustomMetricNamespace"
                },
                "Statistic": "SampleCount",
                "Period": 60,
                "Threshold": 5,
                "AlarmActions": [
                    {
                        "Ref": "TeamEmailTopic"
                    },
                    {
                        "Ref": "ServiceNowTopicArn"
                    }
                ],
                "OKActions": [
                    {
                        "Ref": "TeamEmailTopic"
                    },
                    {
                        "Ref": "ServiceNowTopicArn"
                    }
                ],
                "ComparisonOperator": "GreaterThanOrEqualToThreshold",
                "EvaluationPeriods": 1
            }
        },
        "LambdaErrorAlertHigh": {
            "Type": "AWS::CloudWatch::Alarm",
            "Properties": {
                "AlarmName": {
                    "Fn::Join": [
                        "-",
                        [
                            {
                                "Ref": "FunctionName"
                            },
                            "high-alarm"
                        ]
                    ]
                },
                "AlarmDescription": {
                    "Ref": "CIName"
                },
                "MetricName": {
                    "Ref": "CustomMetricName"
                },
                "Namespace": {
                    "Ref": "CustomMetricNamespace"
                },
                "Statistic": "SampleCount",
                "Period": 300,
                "Threshold": 50,
                "AlarmActions": [
                    {
                        "Ref": "TeamEmailTopic"
                    },
                    {
                        "Ref": "ServiceNowTopicArnHigh"
                    }
                ],
                "OKActions": [
                    {
                        "Ref": "TeamEmailTopic"
                    },
                    {
                        "Ref": "ServiceNowTopicArnHigh"
                    }
                ],
                "ComparisonOperator": "GreaterThanOrEqualToThreshold",
                "EvaluationPeriods": 1
            }
        }
    }
}
