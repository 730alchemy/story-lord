from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    anthropic_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


def initialize_environment():
    """Initialize environment variables from settings."""
    settings = Settings()

    if "ANTHROPIC_API_KEY" not in os.environ:
        os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key

    return settings


# Auto-initialize when module is imported
settings = initialize_environment()
