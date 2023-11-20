from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration"""
    format: str = "%(levelprefix)s | %(asctime)s | %(name)20s | %(message)s"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": format,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "uvicorn.error": {"handlers": ["default"], "level": "INFO", "propagate": False}
    }
    root: dict = {
        "level": "DEBUG",
        "handlers": ["default"],
        "propagate": False
    }
