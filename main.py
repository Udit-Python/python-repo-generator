from ApplicationCommandLiterals import ApplicationCommandLiterals
from ApplicationLiterals import ApplicationLiterals
from create_files import create_files
from create_folders import create_folders
from write_content_to_files import write_content_to_file
from create_template_yaml import create_template_yaml
from create_param_json import create_param_json


def generate_lambda(path):
    create_folders(path)
    create_files(path)

    for file in ApplicationLiterals.file_list:
        commands = ApplicationCommandLiterals.commands.get(file[1:])
        if commands:
            write_content_to_file(path, path + file, commands)

    print("Creating Cloudformation Files....")
    kibana, alarms = create_template_yaml(path)
    create_param_json(path, kibana, alarms)


if __name__ == '__main__':
    repo_name = input("Enter Repo Name : ")
    print(f"Creating Repository with name = {repo_name}")
    generate_lambda(repo_name)
