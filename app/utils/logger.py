import os
import logging
from logging.handlers import RotatingFileHandler

from app.config import get_settings


settings = get_settings()

def check_log_path_exists() -> None:
    """Ensure the log directory exists."""
    if not os.path.exists(settings.log_directory_path):
        os.makedirs(settings.log_directory_path)


def get_app_logger() -> logging.Logger:
    """Return a singleton application logger with file and stream handlers."""
    check_log_path_exists()
    logger = logging.getLogger('local_allocation_manager')
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S'
        )
        file_handler = RotatingFileHandler(
            settings.log_filename_path + ".log",
            maxBytes=10*1024*1024,
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
    return logger