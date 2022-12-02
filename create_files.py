from ApplicationLiterals import ApplicationLiterals


def create_files(path):
    for file in ApplicationLiterals.file_list:
        with open(path + file, 'w'):
            pass


if __name__ == '__main__':
    from create_folders import create_folders
    create_folders("test")
    create_files("test")
