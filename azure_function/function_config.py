# azure_function/function_config.py

from app.config.settings import get_settings

def get_function_settings():
    """
    Returns shared application settings loaded from the .env file.
    This is useful for Azure Functions to consistently access the app's config.
    """
    return get_settings()
