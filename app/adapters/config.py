import os, configparser, pickle


class ConfigNotFound(Exception):
    pass


class ConfigAdapter:
    """
    Abstraction for config management and Exception handling
    """

    @staticmethod
    def deep_copy_config(config):
        """
        Deep copy the config parser object for cases where
        the local config and this object must be different.
        """
        raw_config = pickle.dumps(config)
        return pickle.loads(raw_config)

    @staticmethod
    def get_new_config_parser(interpolation=None):
        """
        TODO - describe this
        """
        return configparser.ConfigParser(interpolation=interpolation)

    @staticmethod
    def read_config_from_file(file_name, parser=None):
        """
        TODO - describe this
        """
        if parser is None:
            parser = ConfigAdapter.get_new_config_parser()
        parser.read(file_name)
        return parser

    def __init__(self, config_dir, config_name):
        self.config_dir = config_dir
        config_path = os.path.join(config_dir, config_name)

        if not os.path.exists(config_path):
            print(
                "No configuration file named {0} found in directory {1}".format(
                    config_dir, config_name
                )
            )
            exit()

        self.config_path = config_path
        self.parser = ConfigAdapter.read_config_from_file(self.config_path)
        print("Config successfully initialised from {0}".format(config_path))

    @property
    def parser(self):
        return ConfigAdapter.deep_copy_config(self.__parser)

    @parser.setter
    def parser(self, parser):
        self.__parser = parser

    def get(self, *args, **kwargs):
        try:
            return self.__parser.get(*args, **kwargs)
        except Exception as e:
            raise ConfigNotFound(
                "No configuration for '{}' in section '{}'".format(args[0], args[1])
            )

    def getboolean(self, *args, **kwargs):
        return self.__parser.getboolean(*args, **kwargs)
