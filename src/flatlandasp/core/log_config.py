import logging
import os
import sys
from functools import lru_cache
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration"""
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "flatlandasp.core.log_config.LoggingFormatter",
            "datefmt": "%H:%M:%S",
        }
    }
    filters: dict = {
        "default": {
            "()": "flatlandasp.core.log_config.PackageRelativePathFilter",
            "base_package": "flatlandasp"
        }
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        }
    }
    loggers: dict = {
        "flasp": {"handlers": ["default"], "filters": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"handlers": ["default"], "filters": ["default"], "level": "INFO", "propagate": False},
        "uvicorn.access": {"handlers": ["default"], "filters": ["default"], "level": "INFO", "propagate": False},
    }
    root: dict = {
        "level": "INFO",
        "handlers": ["default"],
        "propagate": False
    }


class LoggingFormatter(logging.Formatter):
    """ Basic logging formatter with more information and coloring."""
    green = "\x1b[32;1m"
    yellow = "\x1b[33;1m"
    white = "\x1b[37;1m"
    red = "\x1b[31;1m"
    reset = "\x1b[0m"

    format_str = (
        f"%(levelname)-8s{reset} | "
        f"{white}%(relativepath)50s:%(lineno)-4d{reset} | "
        f"%(asctime)s{reset} | "
        f"%(message)s"
    )

    FORMATS = {
        logging.DEBUG: format_str + reset,
        logging.INFO: green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: red + format_str + reset
    }

    def format(self, record):
        """ Create and set the actual formatter and format."""
        log_fmt = self.FORMATS.get(record.levelno, self.format_str)
        formatter = logging.Formatter(log_fmt, datefmt="%H:%M:%S")
        return formatter.format(record)


class PackageRelativePathFilter(logging.Filter):
    def __init__(self, base_package, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_package = base_package
        self.base_package_path = os.path.abspath(
            __import__(base_package).__path__[0])

    def filter(self, record):
        # If pathname is within flatlandasp, make it relative to the package
        if record.pathname.startswith(self.base_package_path):
            package = self.base_package
            path = os.path.relpath(
                record.pathname, self.base_package_path)
            record.relativepath = f"({self.base_package}) {path}"
        # If it is not within flatlandasp, then it must be in
        # the virtual environment
        else:
            venv_path = f"{sys.prefix}\\lib\\site-packages\\"
            relative_path_split = os.path.relpath(
                record.pathname, venv_path).split("\\")
            package = relative_path_split[0]
            path = '\\'.join(relative_path_split[1:])

        record.relativepath = f"({package}) {path}"

        return True


@lru_cache
def get_logger():
    dictConfig(LogConfig().dict())
    return logging.getLogger("flasp")
