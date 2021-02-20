from types import SimpleNamespace


# For nested dot notation dicts
# https://stackoverflow.com/a/54332748/5680716
class NestedNamespace(SimpleNamespace):
    def __init__(self, dictionary, **kwargs):
        super().__init__(**kwargs)
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__setattr__(key, NestedNamespace(value))
            else:
                self.__setattr__(key, value)


class FileOperations():
    MODES = NestedNamespace({
        "WRITE": "w"
    })
    
    @staticmethod
    def write(filename, content, write_function):
        access_mode = FileOperations.MODES.WRITE
        with open(filename, access_mode) as open_file:
            write_function(open_file, content)
