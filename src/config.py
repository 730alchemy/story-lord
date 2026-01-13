import logging
import os

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str

    model_config = SettingsConfigDict(env_file=".env")


def configure_logging():
    """Configure structlog with stdlib logging integration."""
    # Configure stdlib logging
    logging.basicConfig(format="%(message)s", level=logging.INFO)

    # Suppress noisy HTTP client logs
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Get default columns and reorder: timestamp, level, logger, event, context vars
    default_renderer = structlog.dev.ConsoleRenderer()
    default_columns = {c.key: c for c in default_renderer._columns}
    columns = [
        default_columns["timestamp"],
        default_columns["level"],
        default_columns["logger"],
        default_columns["event"],
        structlog.dev.Column("", default_renderer._default_column_formatter),
    ]

    # Configure structlog to use stdlib
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(columns=columns),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def initialize_environment():
    """Initialize environment variables from settings."""
    settings = Settings()

    if "ANTHROPIC_API_KEY" not in os.environ:
        os.environ["ANTHROPIC_API_KEY"] = settings.anthropic_api_key

    return settings


# Auto-initialize when module is imported
configure_logging()
settings = initialize_environment()
