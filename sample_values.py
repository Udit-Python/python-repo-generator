def get_lambda_sample_code(path):
    lambda_code = f"""
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

env = os.environ["environment"]


def lambda_handler(event, context):
    try:
        print("Inside {path} Lambda !!!", event)
        print("Environment = ", env)
        return 'Lambda execution success!'
    except Exception as e:
        print('Error Occurred in lambda  Record :: ', e)
        logger.exception(e)
    finally:
        logger.info('End of {path} lambda')

"""
    return lambda_code


def get_lambda_test_sample_code():
    lambda_test_code = f"""
import os
import pytest

@pytest.fixture(autouse=True)
def env_fixture(mocker):
    os.environ['environment'] = 'devl'


def test_lambda_handler_exists():
    from python_function.function.lambdafunction import lambda_handler
    assert str(type(lambda_handler)) == "<class 'function'>"
    
def test_lambda_handler_method_success_scenario(mocker):
    from python_function.function.lambdafunction import lambda_handler
    result = lambda_handler(None, None)
    assert result == 'Lambda execution success!'

"""

    return lambda_test_code
