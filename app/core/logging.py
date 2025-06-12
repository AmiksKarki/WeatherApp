import logging
import sys

from app.core.config import settings


def setup_logging() -> logging.Logger:
    """Setup logging configuration"""

    # Log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper())

    # Configure logging
    logging.basicConfig(
        level=log_level, format=log_format, handlers=[logging.StreamHandler(sys.stdout)]
    )

    # Create and configure logger
    logger = logging.getLogger("weatherpy")
    logger.setLevel(log_level)

    # Return configured logger
    return logger
