import logging
import sys
import os

from utils import NestedNamespace


class LoggingAdapter():
    # TODO - Implement alternate error streams

    VALUES = NestedNamespace({
        "CONFIG_SECTION": "logging"
    })

    def __init__(self, config):
        self.logger_name = config.get(
            self.VALUES.CONFIG_SECTION, "logger_name")
        self.logger = logging.getLogger(self.logger_name)
        # Let handlers decide what level to publish & where
        self.logger.setLevel(logging.DEBUG)
        self.__prepare_formatter(config)
        self.__prepare_handlers(config)

    def __prepare_formatter(self, config):
        format_string = config.get(
            self.VALUES.CONFIG_SECTION, "formatter")
        self.formatter = logging.Formatter(format_string)

    def __prepare_handlers(self, config):
        # Configure Console
        console_enabled = config.getboolean(
            self.VALUES.CONFIG_SECTION, "console_enabled")
        if console_enabled:
            HandlerClass = logging.StreamHandler
            destination = sys.stdout
            level = config.get(
                self.VALUES.CONFIG_SECTION, "console_level")
            formatter = self.formatter
            self.__configure_handler(
                HandlerClass, destination, level, formatter)

        # Configure File
        file_enabled = config.getboolean(
            self.VALUES.CONFIG_SECTION, "console_enabled")
        if file_enabled:
            HandlerClass = logging.FileHandler
            file_directory = config.get(
                self.VALUES.CONFIG_SECTION, "file_directory")
            file_name = config.get(
                self.VALUES.CONFIG_SECTION, "file_name")
            destination = os.path.join(file_directory, file_name)
            level = config.get(
                self.VALUES.CONFIG_SECTION, "file_level")
            formatter = self.formatter
            self.__configure_handler(
                HandlerClass, destination, level, formatter)

    def __configure_handler(self, HandlerClass, destination, level, formatter):
        handler = HandlerClass(destination)
        handler.setLevel(level)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
