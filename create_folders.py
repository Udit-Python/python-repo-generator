import os
from ApplicationLiterals import ApplicationLiterals


def create_folders(path):
    os.mkdir(path)
    for folder in ApplicationLiterals.folder_list:
        os.mkdir(path + folder)


if __name__ == '__main__':
    create_folders("test")
