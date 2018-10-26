import json
import os.path


class FileUtility(object):

    def __init__(self):
        pass

    @staticmethod
    def file_exists(file_name: str) -> bool:
        if not file_name:
            raise Exception('File name has to be set')

        return os.path.exists(file_name)

    @staticmethod
    def create_file(file_name: str, content: str) -> None:
        if not file_name:
            raise Exception('File name has to be set')

        f = open(file_name, "w+")
        if content:
            f.write(content)
        f.close()

    @staticmethod
    def read_file_as_dict(file_name: str) -> dict:
        if not FileUtility.file_exists(file_name):
            return {}

        with open(file_name, "r") as file_to_read:
            json_content = file_to_read.read()
            content: dict = json.loads(json_content)

        return content

    @staticmethod
    def create_folder(path) -> None:
        if not os.path.exists(path):
            os.mkdir(path)
        elif not os.path.isdir(path):
            return

    @staticmethod
    def remove_file(path: str) -> None:
        if not os.path.exists(path):
            return
        if not os.path.isdir(path):
            os.remove(path)
        else:
            os.removedirs(path)