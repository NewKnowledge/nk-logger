# nk-logger
A python logger that plays nice with Datadog. It outputs logs using a json formatter, sending `WARNING`, `ERROR`, and `CRITICAL` logs to `stderr` and `DEBUG` and `INFO` logs to `stdout`.

# Basic Usage

pip install `git+https://github.com/NewKnowledge/nk-logger.git@<branch-name or commit-hash>#egg=nk_logger`. Typically, this is done by adding it to `requirements.txt` (pip) or `environment.yml` (conda). Make sure git is installed on the system or container.

At the top of each file that uses a logger, put:
```
from nk_logger import get_logger
logger = get_logger(__name__)
```

Then use like:
```
logger.debug("this is content that usually won't be relevant")
logger.info("this is important information")
logger.info(f"here is information about this variable: {var}")
logger.warning("something might be wrong here")
logger.error("oh no, an error!")
logger.exception("oh no, an error! let's log the stack trace.")
```
Note that `logger.exception(message)` is equivalent to `logger.error(message, exc_info=True)` and will automatically attach the exception information to the log.

The `nk_logger` module reads the `LOG_LEVEL` and `SERVICE_NAME` environment variables and does basic configuration on module import.

# Configure
The `nk_logger` module has two config parameters: `level` and `prefix`. By default they are set by the environment variables `LOG_LEVEL` and `SERVICE_NAME` upon import if they are provided, otherwise they are set to 'INFO' and '' respectively. By default the root logger's log level is also set to the same `level`. The `config_logger` function allows you to optionally override those defaults and explicitly set the default `level`, `prefix`, or `root_log_level`. Specifying the `root_log_level` allows the root logger to have a different level than the loggers generated by `get_logger`; this is useful for exposing (or muting) third-party logs (e.g. from `kafka` or `requests`).

An example setup that would allow us to keep our own 'INFO' logs, but silence third-party logs below 'WARNING':

```
from nk_logger import config_logger
config_logger(level="INFO", root_log_level="WARNING")
```

If instead we are using a `config.py` file and want to keep third-party logs, the usage might look like:

```
from config import LOG_LEVEL, SERVICE_NAME
from nk_logger import config_logger, get_logger

config_logger(level=LOG_LEVEL, prefix=SERVICE_NAME)
logger = get_logger(__name__)
```



# Details
Upon configuration, `nk_logger` creates two log handlers: `out_handler` and `err_handler`. `out_handler` writes logs to stdout and filters out logs above 'INFO'. `err_handler` writes logs to stderr and ignores logs below 'WARNING'. Both handlers are attached to the root logger and set to the given log `level`. Any new logger created is not given any handlers, so will pass its logs up to the root logger's handlers to be processed. Third-party logs are also sent to the root logger and processed by the same handlers as internal logs, so they are also json-formatted.
