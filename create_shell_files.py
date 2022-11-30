def create_shell_files(path):
    initial_commands = ['#!/bin/bash', 'set -eo pipefail']

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

    with open(f"{path}/build-layer.sh", 'w') as build_file:
        for build_layer_command in initial_commands + build_layer_commands:
            build_file.write(build_layer_command + "\n")

    with open(f"{path}/test-setup.sh", 'w') as setup_file:
        for setup_command in initial_commands + test_setup_commands:
            setup_file.write(setup_command + "\n")

    with open(f"{path}/run-unit-tests.sh", 'w') as unit_test_file:
        for unit_test in initial_commands + run_unit_test_commands:
            unit_test_file.write(unit_test + "\n")

    with open(f"{path}/run-integration-tests.sh", 'w') as integration_test_file:
        for integration_test in initial_commands + run_integration_test_commands:
            integration_test_file.write(integration_test + "\n")


def create_deployment_shell_script(path):
    print("Start Creating Deployment Shell Files...")

    s3_bucket_for_cf = input("Enter Bucket Name [XXX-XXXX-XXXX-env]: ")
    region = input("Enter AWS Region [default - us-east-1] : ")
    stack_name = input("Enter Stack Name [XXXX-XXXX-XXXX-env] : ")

    final_bucket_name = f"{s3_bucket_for_cf}-$env"
    final_stack_name = f"{stack_name}-$env"

    if not region:
        region = 'us-east-1'

    initial_commands = ['#!/bin/bash', 'set -eo pipefail']

    deploy_file_commands = [
        "env=$1",
        f'aws s3 mb s3://{final_bucket_name}',
        f'ARTIFACT_BUCKET={final_bucket_name}',
        f'aws cloudformation package --template-file template.yml --s3-bucket $ARTIFACT_BUCKET '
        f'--output-template-file out.yml --region {region}',
        f'aws cloudformation deploy --template-file out.yml --stack-name {final_stack_name} --capabilities'
        f' CAPABILITY_NAMED_IAM --region {region} --parameter-overrides file://aws_cloudformation_params/$env.json'
    ]

    with open(f"{path}/deploy.sh", 'w') as deploy_file:
        for command in initial_commands + deploy_file_commands:
            deploy_file.write(command + "\n")




