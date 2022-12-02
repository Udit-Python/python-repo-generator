from prepare_deploy_shell_commands import prepare_deploy_shell_commands
from sample_lambda_code import get_lambda_sample_code, get_lambda_test_sample_code


class ApplicationCommandLiterals:
    gitignore_content = [
        '.idea', '__pycache__', 'virtual', 'test', '**/.pytest_cache', '.coverage', 'htmlcov', 'junit',
        '.scannerwork', 'coverage.xml', '.vscode'
    ]
    requirements = [
        'boto3', 'requests', 'psycopg2-binary', 'aws-xray-sdk==2.4.3'
    ]
    test_requirements = [
        'pytest', 'pytest-cov', 'pytest-html', 'pytest-mock', 'moto', 'patch', 'Mock', 'pyyaml'
    ]
    initial_shell_commands = ['#!/bin/bash', 'set -eo pipefail']
    build_layer_commands = [
        'rm -rf package', 'cd python_function',
        'python3 -m pip install --target ../package/python -r ./function/requirement.txt'
    ]
    test_setup_commands = [
        "python3 -m pip install --upgrade pip --user",
        'echo "************************************* INSTALL DEPENDENCIES FOR TESTS **************************"',
        "python3 -m pip install -r requirement.txt --user"
    ]
    run_unit_test_commands = [
        'python3 -m pytest ./unit_test/ --cov=python_function/ -v  --cov-report=xml --cov-report=html',
        'python3 -m coverage report -m --omit=*test*'
    ]
    run_integration_test_commands = [
        'echo "************************************* INTEGRATION TEST [START]   *****************************"',
        'python3 -m pytest ./integration_test/ -v',
        'echo "************************************* INTEGRATION TEST [END]     *****************************"'
    ]
    deploy_file_commands = [
        "env=$1",
        'aws s3 mb s3://{}',
        'ARTIFACT_BUCKET={}',
        'aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET '
        '--output-template-file out.yml --region {}',
        'aws cloudformation deploy --template-file out.yml --stack-name {} --capabilities'
        ' CAPABILITY_NAMED_IAM --region {} --parameter-overrides file://aws_cloudformation_params/$env.json'
    ]

    sonar_commands = [
        "sonar.projectKey={}",
        "sonar.projectName={}",
        "sonar.projectVersion=1.0",
        "sonar.language=py",
        "sonar.host.url=http://localhost:3000",
        "sonar.sources=python_function/function",
        "sonar.sourceEncoding=UTF-8",
        "sonar.python.coverage.reportPaths=coverage.xml",
        "sonar.python.version=3.8,3.9"
    ]

    commands = {
        '.gitignore': gitignore_content,
        'requirement.txt': test_requirements + requirements,
        'build-layer.sh': initial_shell_commands + build_layer_commands,
        'test-setup.sh': initial_shell_commands + test_setup_commands,
        'run-unit-tests.sh': initial_shell_commands + run_unit_test_commands,
        'run-integration-tests.sh': initial_shell_commands + run_integration_test_commands,
        'deploy.sh': prepare_deploy_shell_commands,
        'python_function/function/__init__.py': ["# Project {} V0.0.1"],
        'python_function/function/lambda_function.py': get_lambda_sample_code,
        'python_function/function/requirement.txt': requirements,
        'unit_test/__init__.py': [
            "# Project {} V0.0.1", "# Test Command :: pytest ./unit_test/ --cov=python_function/ -v"
        ],
        'unit_test/lambda_function_test.py': get_lambda_test_sample_code,
        'integration_test/__init__.py': [
            "# Project {} V0.0.1", "# Test Command :: pytest ./integration_test/ -v"
        ],
        'sonar-project.properties': sonar_commands

    }


if __name__ == '__main__':
    print(ApplicationCommandLiterals.commands.get('requirement.txt'))
