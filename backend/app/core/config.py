from pydantic_settings import BaseSettings
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Inventory Management API"
    
    # Database - Railway provides DATABASE_URL environment variable
    # No hardcoded fallback - must be set in production
    DATABASE_URL: str = ""
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS - Allow Railway domain and localhost for development
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://localhost:3000",
        "https://127.0.0.1:3000",
        "https://*.railway.app",  # Allow Railway domains
        "https://*.up.railway.app",  # Allow Railway domains
        "https://inventory-management-production-82d5.up.railway.app",  # Specific Railway domain
        "*"  # Allow all origins for now, can be restricted later
    ]
    
    # Debug
    DEBUG: bool = True
    
    # Port - Railway provides PORT environment variable
    PORT: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Post-process settings to handle Railway-specific configurations
def post_process_settings():
    """Post-process settings after initialization"""
    # Explicitly read DATABASE_URL from environment variable
    env_database_url = os.getenv("DATABASE_URL")
    if env_database_url:
        settings.DATABASE_URL = env_database_url
        logger.info("Using DATABASE_URL from environment variable")
    else:
        logger.warning("DATABASE_URL environment variable is not set")
    
    # Explicitly read PORT from environment variable
    env_port = os.getenv("PORT")
    if env_port:
        settings.PORT = int(env_port)
        logger.info(f"Using PORT from environment variable: {settings.PORT}")
    
    # Log configuration for debugging
    logger.info(f"Initial Database URL: {settings.DATABASE_URL[:20]}..." if settings.DATABASE_URL else "NOT SET")
    logger.info(f"Port: {settings.PORT}")
    logger.info(f"Debug: {settings.DEBUG}")
    
    # Handle Railway's DATABASE_URL format (might need to add sslmode)
    if settings.DATABASE_URL and settings.DATABASE_URL.startswith("postgres://"):
        settings.DATABASE_URL = settings.DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # Add sslmode if not present (for Railway)
    if settings.DATABASE_URL and "sslmode=" not in settings.DATABASE_URL:
        if "?" in settings.DATABASE_URL:
            settings.DATABASE_URL += "&sslmode=require"
        else:
            settings.DATABASE_URL += "?sslmode=require"
    
    logger.info(f"Final Database URL: {settings.DATABASE_URL[:20]}..." if settings.DATABASE_URL else "NOT SET")

# Call post-processing
post_process_settings()
