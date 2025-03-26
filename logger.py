import logging
import structlog
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Get environment
ENV = os.getenv("ENV", "development")

# Configure log levels based on environment
LOG_LEVELS: Dict[str, int] = {
    "development": logging.DEBUG,
    "test": logging.INFO,
    "staging": logging.INFO,
    "production": logging.WARNING
}

# Configure structlog processors based on environment
def get_processors() -> list:
    base_processors = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if ENV == "development":
        base_processors.append(structlog.processors.ConsoleRenderer())
    else:
        base_processors.append(structlog.processors.JSONRenderer())

    return base_processors

# Configure structlog
structlog.configure(
    processors=get_processors(),
    wrapper_class=structlog.make_filtering_bound_logger(LOG_LEVELS.get(ENV, logging.INFO)),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

# Configure standard logging with rotation
def setup_file_handler() -> RotatingFileHandler:
    handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8',
        mode='a'  # Append mode
    )
    handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    return handler

# Configure standard logging
logging.basicConfig(
    level=LOG_LEVELS.get(ENV, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        setup_file_handler(),
        logging.StreamHandler()
    ]
)

# Create logger
logger = structlog.get_logger()

# Write initial log entry with environment info
logger.info(
    "Logging system initialized",
    environment=ENV,
    log_level=logging.getLevelName(LOG_LEVELS.get(ENV, logging.INFO))
)
