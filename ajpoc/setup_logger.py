#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module performs all the logging related configuration
"""
from logging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging import Logger, getLogger, Formatter, StreamHandler, FileHandler
from json import load
from sys import stdout
from scrapy.settings import default_settings


def import_logger_settings() -> dict:
    """
    This function gets the logging settings from the configuration json file.
    :return: It returns a dictionary with the logger settings.
    """
    with open('config/config.json') as config_json_file:
        logger_data = load(config_json_file).get("logger")
        return logger_data


def logger_level_mapper(level_str: str) -> int:
    """
    This function parses the logging level from the String representation to
    its integer value. Accepted levels are: 'NOTSET', 'DEBUG', 'INFO',
    'WARNING', 'ERROR' and 'CRITICAL'.
    :param level_str: The string representation of the logging level.
    :return: The integer value of the logging level.
    """
    levels = {
        'NOTSET': NOTSET,
        'DEBUG': DEBUG,
        'INFO': INFO,
        'WARNING': WARNING,
        'ERROR': ERROR,
        'CRITICAL': CRITICAL
    }
    return levels.get(level_str, NOTSET)


def setup_module_logger(module_name: str) -> Logger:
    """
    This function configures a logger with the name passed as argument and the
    settings defined in the configuration json file.
    :param module_name: String with the name of the module which is going to
    use the logger.
    :return: The configured logger.
    """
    # Import logger settings from config file
    logger_config = import_logger_settings()

    # Setup module logger
    logger = getLogger(module_name)
    formatter = Formatter(fmt=logger_config.get("log_fmt"),
                          datefmt=logger_config.get("date_fmt"))
    # Console output
    if logger_config.get("console_appender") and \
            not (logger_config.get("detailed_log") and
                 not logger_config.get("file_appender")):
        console_handler = StreamHandler(stdout)
        console_handler.setLevel(
            logger_level_mapper(logger_config.get("console_level")))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File output
    if logger_config.get("file_appender") and \
            not logger_config.get("detailed_log"):
        file_handler = FileHandler(logger_config.get("log_file"), "w")
        file_handler.setLevel(
            logger_level_mapper(logger_config.get("file_level")))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    # Return the configured logger
    return logger


def get_scrapy_logger_settings(extra_settings: dict = None) -> dict:
    """
    This function will populate and return a dictionary, being the keys the
    name of the scrapy logging settings and its values set based on the options
    defined in the configuration json file. If a dictionary is passed as
    argument, the returned dictionary will contain all its keys and the new
    logging related ones.
    :param extra_settings: Optional dictionary to which add the settings.
    :return: A dictionary with all the settings
    """
    # Import logger settings from config file
    logger_config = import_logger_settings()

    # Create an empty dictionary if not passed as argument
    if extra_settings is not None:
        settings = extra_settings
    else:
        settings = {}

    # Configure the logging settings
    # [LOG_LEVEL]
    # Available levels are CRITICAL, ERROR, WARNING, INFO and DEBUG
    if logger_config.get("console_appender") and not logger_config.get(
            "file_appender"):
        settings['LOG_LEVEL'] = logger_config.get("console_level")
    elif not logger_config.get("console_appender") and logger_config.get(
            "file_appender"):
        settings['LOG_LEVEL'] = logger_config.get("file_level")
    else:
        if logger_level_mapper(
                logger_config.get("console_level")) <= logger_level_mapper(
                    logger_config.get("file_level")):
            settings['LOG_LEVEL'] = logger_config.get("console_level")
        else:
            settings['LOG_LEVEL'] = logger_config.get("file_level")

    # [LOG_ENABLED]
    if logger_config.get("detailed_log") and \
            (logger_config.get("console_appender") or
             logger_config.get("file_appender")):
        settings['LOG_ENABLED'] = True
    else:
        settings['LOG_ENABLED'] = False
        return settings

    # [LOG_ENCODING]
    # The encoding to use for the logging
    settings['LOG_ENCODING'] = logger_config.get("log_encoding")

    # [LOG_FORMAT]
    # String for log formatting as described in the Python logging
    # documentation
    settings['LOG_FORMAT'] = logger_config.get("log_fmt")

    # [LOG_DATEFORMAT]
    # String for date/time formatting, expansion of the '%(ascitime)s'
    # placeholder in [LOG_FORMAT]
    settings['LOG_DATEFORMAT'] = logger_config.get("date_fmt")

    # [LOG_STDOUT]
    # If True, all standard output and error of the process will be redirected
    # to the log.
    settings['LOG_STDOUT'] = False

    # [LOG_SHORT_NAMES]
    # If True the logs will just contain the root path, if False it displays
    # the component responsible for the log.
    settings['LOG_SHORT_NAMES'] = False

    # [LOG_FILE]
    # File name to use for logging output. If None, standard error will be
    # used.
    if logger_config.get("file_appender"):
        settings['LOG_FILE'] = logger_config.get("log_file")

    # Return the configured settings
    return settings


def setup_scrapy_logger():
    """
    This function configures the default scrapy logger settings with the values
    of the dictionary returned by the ``get_scrapy_logger_settings`` method.
    """
    scrapy_logger_settings = get_scrapy_logger_settings()
    default_settings.LOG_ENABLED = scrapy_logger_settings.get('LOG_ENABLED')
    default_settings.LOG_LEVEL = scrapy_logger_settings.get('LOG_LEVEL')
    default_settings.LOG_ENCODING = scrapy_logger_settings.get('LOG_ENCODING')
    default_settings.LOG_FORMAT = scrapy_logger_settings.get('LOG_FORMAT')
    default_settings.LOG_DATEFORMAT = scrapy_logger_settings.get(
        'LOG_DATEFORMAT')
    default_settings.LOG_STDOUT = scrapy_logger_settings.get('LOG_STDOUT')
    default_settings.LOG_SHORT_NAMES = scrapy_logger_settings.get(
        'LOG_SHORT_NAMES')
    default_settings.LOG_FILE = scrapy_logger_settings.get('LOG_FILE')
