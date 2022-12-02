from sample_lambda_code import get_lambda_sample_code, get_lambda_test_sample_code


def create_lambda_and_lambda_test(path):
    lambda_code = get_lambda_sample_code(path)
    with open(f"{path}/python_function/function/lambdafunction.py", 'w') as lambda_file:
        lambda_file.write(lambda_code)

    lambda_test_code = get_lambda_test_sample_code()
    with open(f"{path}/unit_test/lambda_function_test.py", 'w') as lambda_test_file:
        lambda_test_file.write(lambda_test_code)

