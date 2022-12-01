def create_sonar_file(path):
    print("Creating Sonar-project.properties ....")
    sonar_host = input("Enter Sonar Host :: ")

    sonar_commands = [
        f"sonar.projectKey={path}",
        f"sonar.projectName={path}",
        "sonar.projectVersion=1.0",
        "sonar.language=py",
        f"sonar.host.url={sonar_host}",
        "sonar.sources=python_function/function",
        "sonar.sourceEncoding=UTF-8",
        "sonar.python.coverage.reportPaths=coverage.xml",
        "sonar.python.version=3.8,3.9"
    ]

    with open(f"{path}/sonar-project.properties", 'w') as sonar_file:
        for sonar_command in sonar_commands:
            sonar_file.write(sonar_command + "\n")
