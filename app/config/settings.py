# app/config/settings.py

import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Determine which .env file to load based on FUNCTION_ENVIRONMENT
env = os.getenv("FUNCTION_ENVIRONMENT", "development").lower()
env_file_name = f".env.{env}" if os.path.exists(f".env.{env}") else ".env"


class Settings(BaseSettings):
    # Azure OpenAI Settings
    azure_openai_api_key: str = Field(..., description="Azure OpenAI API key")
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    azure_openai_deployment_name: str = Field(..., description="Azure OpenAI deployment name")
    azure_openai_embedding_deployment: str = Field(..., description="Azure OpenAI embedding deployment")
    azure_openai_api_version: str = Field(..., description="Azure OpenAI API version")

    # Azure Function Settings
    function_environment: str = Field(default="development", description="Function environment")
    function_enable_logging: bool = Field(default=False, description="Enable logging")
    function_enable_prompt_validation: bool = Field(default=True, description="Enable prompt validation")
    function_enable_relevance_validation: bool = Field(default=True, description="Enable relevance validation")

    # App Insights
    appinsights_connection_string: str = Field(default="", description="Azure Application Insights connection string")

    model_config = SettingsConfigDict(env_file=env_file_name)

    @field_validator("*", mode="before")
    @classmethod
    def not_empty(cls, v, info):
        if isinstance(v, str) and not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v


def get_settings() -> Settings:
    return Settings()
