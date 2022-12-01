import copy
import json
import time


def create_param_json(path, kibana_created, alarms_created):
    print("Creating Parameter Json Files ....")
    environments = ['devl', 'qual', 'cert', 'prod']
    time.sleep(1)

    parameter_skeletons = {
        'fn_name': "FunctionName={}",
        'fn_role': "LambdaRoleARN={}",
        'fn_env': "Environment={}",
        'sg': "SecurityGroupId={}",
        'subnets': "VpcSubnetIds={}",
        'component': 'ComponentName={}',
        'layer': 'LayerName={}'
    }

    alarm_skeleton = {
        'email_topic': 'TeamEmailTopic={}',
        'metric_name': "CustomMetricName={}",
        'metric_name_space': 'CustomMetricNamespace={}',
        'service_now_arn': 'ServiceNowTopicArn={}',
        'service_now_high_arn': 'ServiceNowTopicArnHigh={}',
        'ci_name': 'CIName={}'
    }

    if kibana_created and kibana_created == 'Y':
        parameter_skeletons = parameter_skeletons | {'kibana_role': 'KibanaRole={}'}

    if alarms_created and alarms_created == 'Y':
        parameter_skeletons = parameter_skeletons | alarm_skeleton

    print("Enter Common configuration.....")
    fn_name = input("Enter Function Name [XXX-XXX-env] :: ")
    component = input("Enter Component Tag :: ")
    layer_name = fn_name + '-lib'

    for env in environments:
        parameter_skeleton = copy.deepcopy(parameter_skeletons)
        consent = input(f"Do you want to enter {env} env parameters ? (Y/N)")
        security_grps = ''
        fn_role, subnets = '', ''

        if consent and consent == 'Y':
            fn_role = input("Enter Function Role full ARN :: ")
            security_grps = input("Enter Security Group ID ::[sg-XXX]:: ")
            subnets = input("Enter Subnets [Comma separated] :: ")

        parameter_skeleton['fn_name'] = parameter_skeleton['fn_name'].format(fn_name + "-" + env)
        parameter_skeleton['fn_role'] = parameter_skeleton['fn_role'].format(fn_role)
        parameter_skeleton['fn_env'] = parameter_skeleton['fn_env'].format(env)
        parameter_skeleton['sg'] = parameter_skeleton['sg'].format(security_grps)
        parameter_skeleton['subnets'] = parameter_skeleton['subnets'].format(subnets)
        parameter_skeleton['component'] = parameter_skeleton['component'].format(component)
        parameter_skeleton['layer'] = parameter_skeleton['layer'].format(layer_name)

        with open(f"{path}/aws_cloudformation_params/{env}.json", 'w') as env_file:
            aws_json_format = []
            for key in parameter_skeleton:
                aws_json_format.append(parameter_skeleton[key])

            env_file.write(json.dumps(aws_json_format))
