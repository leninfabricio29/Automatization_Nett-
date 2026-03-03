"""Configuration module for RPA Automatization."""

from config.settings import Settings, get_settings
from config.db_config import DatabaseConfig


__all__ = [
    "Settings",
    "get_settings",
    "DatabaseConfig",
]
