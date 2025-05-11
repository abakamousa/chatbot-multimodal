# app/utils/helpers.py

import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.config.settings import get_settings


def get_logger(name: str) -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if settings.function_enable_logging and settings.appinsights_connection_string:
        handler = AzureLogHandler(connection_string=settings.appinsights_connection_string)
        logger.addHandler(handler)
    
    return logger
