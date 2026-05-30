# -----------------------------
# import libraries
# -----------------------------
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# -----------------------------
# LOG DIRECTORY SETUP
# -----------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "pipeline.log")
# -----------------------------
# LOGGER CONFIGURATION
# -----------------------------
def setup_logger(name: str) -> logging.Logger:
    logger =logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Prevent duplicate handlers
    if logger.handlers:
        logger.handlers.clear()

    # -----------------------------
    # Formatter Configuration
    # -----------------------------
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s'
    )

    # -----------------------------
    # File Handler Configuration
    # -----------------------------
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # -----------------------------
    # Console Handler Configuration
    # -----------------------------
    console_handler =logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger