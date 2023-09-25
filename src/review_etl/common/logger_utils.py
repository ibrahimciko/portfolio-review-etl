import logging
from logging import FileHandler
from logging import StreamHandler
from typing import Union
from pathlib import Path
import os
import datetime as dt


def setup_logger(name: str, logs_folder: Union[str, Path]) -> str:
    """Configure logging package to save logs to txt
    Args:
        name (str): name of the logger used by the application
        logs_folder (Union[str, Path]): path where the logs will be stored

    Returns:
        str: name of the logger
    """
    app_logger = logging.getLogger(name)
    if any(isinstance(h, FileHandler) for h in app_logger.handlers):
        # Logging already configured
        return ""

    log_level = logging.DEBUG
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s: %(levelname)-8s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    app_logger.setLevel(log_level)

    # Configure file handler
    filename = "log_{}.txt".format(dt.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    filepath = os.path.join(logs_folder, filename)
    os.makedirs(logs_folder, exist_ok=True)
    file_handler = FileHandler(filepath)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    # Configure console handler
    console_handler = StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)
    return app_logger.name
