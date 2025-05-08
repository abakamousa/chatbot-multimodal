# app/config/settings.py

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    azure_openai_api_key: str = Field(..., description="Azure OpenAI API key")
    azure_openai_endpoint: str = Field(..., description="Azure OpenAI endpoint URL")
    azure_openai_deployment_name: str = Field(..., description="Azure OpenAI deployment name")
    azure_openai_embedding_deployment: str = Field(..., description="Azure OpenAI embedding deployment")
    azure_openai_api_version: str = Field(..., description="Azure OpenAI API version")

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("*", mode="before")
    @classmethod
    def not_empty(cls, v, info):
        if isinstance(v, str) and not v.strip():
            raise ValueError(f"{info.field_name} must not be empty")
        return v

def get_settings():
    return Settings()
