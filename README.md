# nk-logger
A python logger that plays nice with Datadog. It outputs logs using a json formatter, sending `WARNING`, `ERROR`, and `CRITICAL` logs to `stderr` and `DEBUG` and `INFO` logs to `stdout`.

# usage

pip install `git+https://github.com/NewKnowledge/nk-logger.git@<branch-name or commit-hash>#egg=nk_logger`. Typically, this is done by adding it to `requirements.txt` (pip) or `environment.yml` (conda). Make sure git is installed on the system or container.

At the top of each file that uses a logger, put:
```
from nk_logger import get_logger
logger = get_logger(__name__)
```

You can set the log level and service name using `set_logger_config`, e.g. in `config.py`:
```
from nk_logger import set_logger_config
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
SERVICE_NAME = os.environ.get("SERVICE_NAME", "app")
set_logger_config(LOG_LEVEL, SERVICE_NAME)
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
