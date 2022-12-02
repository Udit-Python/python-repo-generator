def create_git_ignore(path):
    ignore_list = [
        '.idea', '__pycache__', 'virtual', 'test', '**/.pytest_cache', '.coverage',
        'htmlcov', 'junit', '.scannerwork', 'coverage.xml', '.vscode'
    ]

    with open(f"{path}/.gitignore", 'w') as file:
        for ignore in ignore_list:
            file.write(ignore)
            file.write("\n")
