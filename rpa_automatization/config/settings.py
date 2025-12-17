"""
Configuration settings for the RPA Automatization project.
Loads environment variables from .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="rpa_automatization", alias="DB_NAME")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="", alias="DB_PASSWORD")
    db_pool_size: int = Field(default=10, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=20, alias="DB_MAX_OVERFLOW")
    
    # Application Settings
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Playwright Settings
    playwright_headless: bool = Field(default=False, alias="PLAYWRIGHT_HEADLESS")
    playwright_timeout: int = Field(default=30000, alias="PLAYWRIGHT_TIMEOUT")
    
    # Login Settings
    login_url: str = Field(default="https://erp.nettplus.net/", alias="LOGIN_URL")
    login_username: str = Field(default="", alias="LOGIN_USERNAME")
    login_password: str = Field(default="", alias="LOGIN_PASSWORD")
    
    # Session Settings
    session_storage_path: str = Field(default="./sesion", alias="SESSION_STORAGE_PATH")
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        populate_by_name = True
    
    @property
    def database_url(self) -> str:
        """Generate PostgreSQL connection URL."""
        return (
            f"postgresql+psycopg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"
    
    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.app_debug and not self.is_production


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure only one instance is created.
    """
    return Settings()
