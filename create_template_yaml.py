import ruamel.yaml

from template_samples import template_params, template_resources
from template_samples import template_resources_kibana, template_resources_alarms


def create_template_yaml(path):
    print("Creating Template.yaml ....")

    yaml = ruamel.yaml.YAML()
    yaml.default_style = ""

    init_command = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': f'This lambda is for {path}',
        'Transform': 'AWS::Serverless-2016-10-31',
    }

    kibana_ = input("Do You Want to Add Kibana ? (Y/N) :: ")
    if kibana_ and kibana_ == 'Y':
        template_params["Parameters"] = template_params["Parameters"] | template_resources_kibana['params']
        template_resources['Resources']['LambdaFunction']['Properties']['Environment']['Variables'] = \
            template_resources['Resources']['LambdaFunction']['Properties']['Environment']['Variables'] | \
            template_resources_kibana['lambda_env']

        template_resources['Resources']['LambdaFunction']['Properties']['Layers'].append(
            template_resources_kibana['layer'])

    alarm = input("Do You Want to Add Alarms ? (Y/N) :: ")

    if alarm and alarm == 'Y':
        template_params["Parameters"] = template_params["Parameters"] | template_resources_alarms['params']
        template_resources['Resources'] = template_resources['Resources'] | template_resources_alarms['resources']

    final_template = init_command | template_params | template_resources

    with open(f"{path}/template.yml", 'w') as template_file:
        yaml.dump(final_template, template_file)


    return kibana_, alarm