def create_requirements_file(path):
    requirements = [
        'boto3', 'requests', 'psycopg2-binary', 'aws-xray-sdk==2.4.3'
    ]

    test_requirements = [
        'pytest', 'pytest-cov', 'pytest-html', 'pytest-mock', 'moto', 'patch', 'Mock', 'pyyaml',
    ]

    test_requirements.extend(requirements)

    with open(f"{path}/requirement.txt", 'w') as test_req_file:
        for test_requirement in test_requirements:
            test_req_file.write(test_requirement + "\n")

    with open(f"{path}/python_function/function/requirement.txt", 'w') as req_file:
        for requirement in requirements:
            req_file.write(requirement + "\n")
