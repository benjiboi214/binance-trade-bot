import json

from types import SimpleNamespace


class NestedNamespace(SimpleNamespace):
    '''
    Used for achieving JS-like dot notated dicts in python.
    implementation pulled from: https://stackoverflow.com/a/54332748/5680716
    '''

    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


class FileOperations():
    '''
    Mostly static based class used for common file operations
    '''
    MODES = NestedNamespace({
        "WRITE": "w",
        "READ": "r"
    })

    @staticmethod
    def read_json(open_file):
        return json.load(open_file)

    @staticmethod
    def write_json(open_file, content):
        json.dump(content, open_file)

    @staticmethod
    def write(filename, content, write_function):
        access_mode = FileOperations.MODES.WRITE
        with open(filename, access_mode) as open_file:
            write_function(open_file, content)

    @staticmethod
    def read(filename, read_function):
        access_mode = FileOperations.MODES.READ
        with open(filename, access_mode) as open_file:
            return read_function(open_file)
