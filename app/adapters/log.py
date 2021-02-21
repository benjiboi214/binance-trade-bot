import logging
import sys
import os

from adapters.config import ConfigAccessor


class LoggingAdapter(ConfigAccessor):
    """
    Abstraction Log management
    Takes config adapter at init and configures the logging for the app appropriately.
    TODO - Implement alternate error streams
    """

    # Strings
    CONFIG_SECTION_NAME = "logging"
    CONFIG_LOGGER_NAME = "logger_name"
    CONFIG_FORMATTER = "formatter"
    CONFIG_CONSOLE_ENABLED = "console_enabled"
    CONFIG_FILE_ENABLED = "file_enabled"
    CONFIG_CONSOLE_LEVEL = "console_level"
    CONFIG_FILE_DIRECTORY = "file_directory"
    CONFIG_FILE_NAME = "file_name"
    CONFIG_FILE_LEVEL = "file_level"

    LOG_SUCCESS_MESSAGE = "Logging successfully initialised"

    def __init__(self, config):
        super().__init__()
        self._save_config(config)

        self.__prepare_logger()
        self.__prepare_formatter()
        self.__prepare_handlers()

        self.logger.debug(LoggingAdapter.LOG_SUCCESS_MESSAGE)

    def __prepare_logger(self):
        self.logger_name = self._get_config(LoggingAdapter.CONFIG_LOGGER_NAME)
        self.logger = logging.getLogger(self.logger_name)
        # Let handlers decide what level to publish & where
        self.logger.setLevel(logging.DEBUG)

    def __prepare_formatter(self):
        format_string = self._get_config(LoggingAdapter.CONFIG_FORMATTER)
        self.formatter = logging.Formatter(format_string)

    def __prepare_handlers(self):
        # Configure Console
        console_enabled = self._get_boolean_config(
            LoggingAdapter.CONFIG_CONSOLE_ENABLED
        )
        if console_enabled:
            HandlerClass = logging.StreamHandler
            destination = sys.stdout
            level = self._get_config(LoggingAdapter.CONFIG_CONSOLE_LEVEL)
            formatter = self.formatter
            self.__configure_handler(HandlerClass, destination, level, formatter)

        # Configure File
        file_enabled = self._get_boolean_config(LoggingAdapter.CONFIG_FILE_ENABLED)
        if file_enabled:
            HandlerClass = logging.FileHandler
            file_directory = self._get_config(LoggingAdapter.CONFIG_FILE_DIRECTORY)
            file_name = self._get_config(LoggingAdapter.CONFIG_FILE_NAME)
            destination = os.path.join(file_directory, file_name)
            level = self._get_config(LoggingAdapter.CONFIG_FILE_LEVEL)
            formatter = self.formatter
            self.__configure_handler(HandlerClass, destination, level, formatter)

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
