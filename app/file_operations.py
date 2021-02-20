class FileOperation():
    
    @staticmethod
    def write(filename, mode, content, write_function):
        with open(filename, mode) as open_file:
            write_function(open_file, content)