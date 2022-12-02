def create_inits(path):
    with open(f"{path}/python_function/function/__init__.py", 'w') as file:
        file.write(f"# Project {path} V0.0.1 \n")

    with open(f"{path}/unit_test/__init__.py", 'w') as file:
        file.write(f"# Project {path} V0.0.1 \n")
        file.write("# Test Command :: pytest ./unit_test/ --cov=python_function/ -v \n")

    with open(f"{path}/integration_test/__init__.py", 'w') as file:
        file.write(f"# Project {path} V0.0.1 \n")
        file.write("# Test Command :: pytest ./integration_test/ -v \n")
