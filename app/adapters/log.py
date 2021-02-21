import logging
import sys
import os


class LoggingAdapter():
    # TODO - Implement alternate error streams
    CONFIG_SECTION_NAME = "logging"

    def __init__(self, config):
        self.logger_name = config.get(
            self.CONFIG_SECTION_NAME, "logger_name")
        self.logger = logging.getLogger(self.logger_name)
        # Let handlers decide what level to publish & where
        self.logger.setLevel(logging.DEBUG)
        self.__prepare_formatter(config)
        self.__prepare_handlers(config)
        self.logger.debug("Logging successfully initialised")

    def __prepare_formatter(self, config):
        format_string = config.get(
            self.CONFIG_SECTION_NAME, "formatter")
        self.formatter = logging.Formatter(format_string)

    def __prepare_handlers(self, config):
        # Configure Console
        console_enabled = config.getboolean(
            self.CONFIG_SECTION_NAME, "console_enabled")
        if console_enabled:
            HandlerClass = logging.StreamHandler
            destination = sys.stdout
            level = config.get(
                self.CONFIG_SECTION_NAME, "console_level")
            formatter = self.formatter
            self.__configure_handler(
                HandlerClass, destination, level, formatter)

        # Configure File
        file_enabled = config.getboolean(
            self.CONFIG_SECTION_NAME, "console_enabled")
        if file_enabled:
            HandlerClass = logging.FileHandler
            file_directory = config.get(
                self.CONFIG_SECTION_NAME, "file_directory")
            file_name = config.get(
                self.CONFIG_SECTION_NAME, "file_name")
            destination = os.path.join(file_directory, file_name)
            level = config.get(
                self.CONFIG_SECTION_NAME, "file_level")
            formatter = self.formatter
            self.__configure_handler(
                HandlerClass, destination, level, formatter)

    def __configure_handler(self, HandlerClass, destination, level, formatter):
        handler = HandlerClass(destination)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def debug(self, *args, **kwargs):
        return self.logger.debug(*args, **kwargs)

    def info(self, *args, **kwargs):
        return self.logger.info(*args, **kwargs)
    
    def warning(self, *args, **kwargs):
        return self.logger.warning(*args, **kwargs)
    
    def error(self, *args, **kwargs):
        return self.logger.error(*args, **kwargs)

    def exception(self, *args, **kwargs):
        return self.logger.exception(*args, **kwargs)
