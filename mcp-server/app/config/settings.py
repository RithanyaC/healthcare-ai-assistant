"""MCP Server configuration"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """MCP Server settings"""
    SERVER_HOST = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
    SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8001))
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # LLM Configuration (for future AI integration)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
    LLM_ENABLED = bool(OPENAI_API_KEY)

settings = Settings()
