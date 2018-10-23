""" Sets up logging config for stream handlers sending info-level logs and
below to stdout and warning-level and above to stderr, provides get_logger
function. Designed to work well with datadog. """

import logging
import os
import sys

from pythonjsonlogger import jsonlogger

LOGGER_CONFIG = {"level": "INFO", "prefix": ""}

_level_str2int = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0}


def init_root_logger(level=LOGGER_CONFIG["level"]):
    """ removes any previous log handlers for root logger, then adds two
    datadog-friendly log handlers to the root logger. one writes to stdout
    and has a log level of the given `level`. The other writes to stderr and
    has a log level of max(WARNING, level). Both use a json formatter. """

    # convert string form to int for comparisons later
    if isinstance(level, str):
        level = _level_str2int[level]

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers = []

    formatter = jsonlogger.JsonFormatter(timestamp=True, reserved_attrs=[])

    # out_handler writes to stdout and handles logs of log level 'INFO' and below
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(formatter)
    out_handler.setLevel(level)
    out_handler.addFilter(lambda record: record.levelno < logging.WARNING)
    root.addHandler(out_handler)

    # err_handler writes to stderr and handles logs of level max('WARNING', `level`) and above
    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setFormatter(formatter)
    err_level = max(logging.WARNING, level)
    err_handler.setLevel(err_level)
    root.addHandler(err_handler)


def set_logger_config(level="INFO", prefix=""):
    """ sets the default level and prefix values for loggers returned by get_logger """
    LOGGER_CONFIG["level"] = level
    LOGGER_CONFIG["prefix"] = prefix


def get_logger(name, level=LOGGER_CONFIG["level"], prefix=LOGGER_CONFIG["prefix"]):
    """ Returns a logger object with given `name` prefixed with `prefix` and log
    level `level`. If level or prefix aren't provided, they are set to
    LOGGER_CONFIG defaults. """

    logger_name = f"{prefix}.{name}" if prefix else name
    return logging.Logger(logger_name, level=level)


# on import, remove any preset log handlers and add dd-friendly handlers to root logger
level = os.getenv("LOG_LEVEL", "INFO")
init_root_logger(level=level)
logger = get_logger(__name__)
logger.info("initialized logger")
