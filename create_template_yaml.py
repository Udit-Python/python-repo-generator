import ruamel.yaml

from template_samples import template_params, template_resources


def create_template_yaml(path):
    print("Creating Template.yaml ....")

    yaml = ruamel.yaml.YAML()
    yaml.default_style = ""

    init_command = {
        'AWSTemplateFormatVersion': '2010-09-09',
        'Description': f'This lambda is for {path}',
        'Transform': 'AWS::Serverless-2016-10-31',
    }

    with open(f"{path}/template.yml", 'w') as template_file:
        yaml.dump(init_command | template_params | template_resources, template_file)
