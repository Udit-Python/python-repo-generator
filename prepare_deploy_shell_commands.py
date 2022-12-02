def prepare_deploy_shell_commands(**kwargs):
    from ApplicationCommandLiterals import ApplicationCommandLiterals
    print("Start Creating Deployment Shell Files...")

    s3_bucket_for_cf = input("Enter Bucket Name [XXX-XXXX-XXXX-env]: ")
    region = input("Enter AWS Region [default - us-east-1] : ")
    stack_name = input("Enter Stack Name [XXXX-XXXX-XXXX-env] : ")

    final_bucket_name = f"{s3_bucket_for_cf}-$env"
    final_stack_name = f"{stack_name}-$env"

    if not region:
        region = 'us-east-1'

    deploy_file_commands = ApplicationCommandLiterals.deploy_file_commands

    deploy_file_commands[1] = deploy_file_commands[1].format(final_bucket_name)
    deploy_file_commands[2] = deploy_file_commands[2].format(final_bucket_name)
    deploy_file_commands[3] = deploy_file_commands[3].format(region)
    deploy_file_commands[4] = deploy_file_commands[4].format(final_stack_name, region)

    return ApplicationCommandLiterals.initial_shell_commands + deploy_file_commands
