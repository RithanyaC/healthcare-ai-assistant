"""
Application configuration and environment variable management.
Supports both development and production environments.
"""
import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

class Environment(str, Enum):
    """Environment types"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class Settings:
    """Application settings loaded from environment variables"""

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == Environment.DEVELOPMENT

    # Server
    SERVER_NAME: str = os.getenv("SERVER_NAME", "Healthcare AI Assistant")
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", 8000))
    API_PREFIX: str = "/api"
    API_VERSION: str = "v1"

    # Database
    DB_DRIVER: str = os.getenv("DB_DRIVER", "sqlite")  # sqlite or postgresql

    # SQLite (default for development)
    if DB_DRIVER == "sqlite":
        DATABASE_URL: str = os.getenv(
            "DATABASE_URL",
            "sqlite:///./healthcare.db"
        )
    else:
        # PostgreSQL configuration (for production)
        DB_USER: str = os.getenv("DB_USER", "healthcare")
        DB_PASSWORD: str = os.getenv("DB_PASSWORD", "password")
        DB_HOST: str = os.getenv("DB_HOST", "localhost")
        DB_PORT: int = int(os.getenv("DB_PORT", 5432))
        DB_NAME: str = os.getenv("DB_NAME", "healthcare_db")
        DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # CORS
    ALLOWED_ORIGINS: list = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:3001"
    ).split(",")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # MCP Server
    MCP_SERVER_URL: str = os.getenv("MCP_SERVER_URL", "http://localhost:8001")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Features
    ENABLE_DATABASE_MIGRATIONS: bool = os.getenv("ENABLE_DATABASE_MIGRATIONS", "true").lower() == "true"
    ENABLE_SAMPLE_DATA: bool = os.getenv("ENABLE_SAMPLE_DATA", "false").lower() == "true"

# Create settings instance
settings = Settings()
