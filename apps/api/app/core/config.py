"""
Application configuration management
"""

import os
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")
    DEBUG: bool = Field(default=False, env="DEBUG")

    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-this", env="SECRET_KEY")
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        env="ALLOWED_ORIGINS",
    )

    # File Storage
    UPLOAD_DIR: str = Field(default="uploads", env="UPLOAD_DIR")
    TEMP_DIR: str = Field(default="temp", env="TEMP_DIR")
    OUTPUT_DIR: str = Field(default="downloads", env="OUTPUT_DIR")
    MAX_FILE_SIZE: int = Field(default=100 * 1024 * 1024, env="MAX_FILE_SIZE")  # 100MB

    # Encryption Settings
    DEFAULT_KEY_SIZE: int = Field(default=32, env="DEFAULT_KEY_SIZE")
    MAX_KEY_SIZE: int = Field(default=64, env="MAX_KEY_SIZE")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s", env="LOG_FORMAT"
    )

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=60, env="RATE_LIMIT_PER_MINUTE")

    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Ensure directories exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.TEMP_DIR).mkdir(exist_ok=True)
Path(settings.OUTPUT_DIR).mkdir(exist_ok=True)
