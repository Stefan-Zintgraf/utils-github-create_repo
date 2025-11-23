"""Logging utilities for the GitHub Repository Creator application."""

from __future__ import annotations

import logging
import os

LOG_DIR = os.path.join(os.getcwd(), "logs")
LOG_FILE_NAME = "application.log"
LOG_FILE = os.path.join(LOG_DIR, LOG_FILE_NAME)


def ensure_log_directory() -> None:
    """Ensure the shared logs directory exists."""
    os.makedirs(LOG_DIR, exist_ok=True)


def configure_logger(name: str = "github_repo_creator", level: int | str = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger writing to the shared log file.

    Args:
        name: Logger name.
        level: Logging level (int or str).
    """
    ensure_log_directory()
    numeric_level = logging.getLevelName(level)
    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    if not any(isinstance(handler, logging.FileHandler) and handler.baseFilename == LOG_FILE for handler in logger.handlers):
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(numeric_level)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
