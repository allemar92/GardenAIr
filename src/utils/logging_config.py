import logging
import os


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "garden_app.log")


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

DEFAULT_LOG_LEVEL = logging.INFO


def setup_logger(name: str = "garden_app") -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(DEFAULT_LOG_LEVEL)

    
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        # File handler
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
