from configparser import ConfigParser

class Parser(object):
    def __init__(self, file_name):
        self._file_name = file_name
        self._parser = ConfigParser()
    
    def parse(self):
        if not self._file_name:
            raise Exception('File name is empty')

        _file = open(self._file_name)

        self._parser.read_file(_file)
    
    def get_value(self, parameter):
        if '.' not in parameter:
            return self._parser[parameter]
        
        path = parameter.split('.')
        if len(path) > 2:
            raise Exception('Path length has to be no longer than 2')
        
        return self._parser[path[0]][path[1]]