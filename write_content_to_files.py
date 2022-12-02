def write_content_to_file(path, file_name, commands):
    with open(file_name, 'w') as file:
        if str(type(commands)) == "<class 'function'>":
            commands = commands(path=path)

        if type(commands) is list:
            for command in commands:
                command = command.format(path)
                file.write(command + "\n")

        else:
            file.write(commands + "\n")
