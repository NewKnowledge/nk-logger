""" Sets up logging config for stream handlers sending info-level logs and
below to stdout and warning-level and above to stderr, provides get_logger
function. Designed to work well with datadog. """

import logging
import sys

from pythonjsonlogger import jsonlogger

LOGGER_CONFIG = {"level": "INFO", "service_name": ""}


def set_logger_config(log_level, service_name):
    LOGGER_CONFIG["level"] = log_level
    LOGGER_CONFIG["service"] = service_name


def get_logger(name, level=LOGGER_CONFIG["level"]):

    formatter = jsonlogger.JsonFormatter(timestamp=True, reserved_attrs=[])
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setLevel(level)
    out_handler.setFormatter(formatter)
    # filter out warning and above, send to stderr instead
    out_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)

    logger = logging.Logger(f"{LOGGER_CONFIG['service']}.{name}", level=level)
    logger.addHandler(out_handler)
    logger.addHandler(err_handler)

    return logger


_logger = get_logger(__name__)
_logger.info("initialized logger")

# remove root logger handlers if it has been given default handler(s)
root_logger = logging.getLogger()
if root_logger.hasHandlers():
    _logger.info(f"removing root logger handlers: {root_logger.handlers}")
    root_logger.handlers = []
