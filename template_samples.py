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
        }
    }
}
