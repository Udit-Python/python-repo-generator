import os

from create_git_ignore import create_git_ignore
from create_inits import create_inits
from create_requirements import create_requirements_file
from create_shell_files import create_shell_files, create_deployment_shell_script
from create_template_yaml import create_template_yaml
from create_param_json import create_param_json
from create_lambda_files import create_lambda_and_lambda_test
from create_sonar_file import create_sonar_file


def print_hi(name):
    print(f'Hi, {name}')
    repo_name = input("Enter Repo Name : ")
    print(repo_name)
    os.mkdir(repo_name)
    os.mkdir(repo_name + "/python_function")
    os.mkdir(repo_name + "/python_function/function")
    os.mkdir(repo_name + "/unit_test")
    os.mkdir(repo_name + "/integration_test")
    os.mkdir(repo_name + '/aws_cloudformation_params')

    create_git_ignore(repo_name)
    create_inits(repo_name)
    create_requirements_file(repo_name)
    create_shell_files(repo_name)
    create_deployment_shell_script(repo_name)
    kibana_created, alarms_created = create_template_yaml(repo_name)
    create_param_json(repo_name, kibana_created, alarms_created)
    create_lambda_and_lambda_test(repo_name)
    create_sonar_file(repo_name)


if __name__ == '__main__':
    print_hi('PyCharm')
