
import logging
import uvicorn

FORMAT: str = "%(levelprefix)s %(asctime)s | %(message)s"

# dictConfig variant
app_dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "basic": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": FORMAT,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "basic",
        },
    },
    "loggers": {
        "simple_example": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


# Code variant to initialize loggers
def init_loggers(logger_name: str = "logger"):
    # Create a logger with the given name
    logger = logging.getLogger(logger_name)

    # Set the logging level
    logger.setLevel(logging.DEBUG)

    # Create a console handler
    console_handler = logging.StreamHandler()

    # Create a formatter using the Uvicorn DefaultFormatter
    formatter = uvicorn.logging.DefaultFormatter(FORMAT)

    # Attach the formatter to the handler
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False

    return logger


log = logging.getLogger("logger")
