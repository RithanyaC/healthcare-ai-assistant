"""
App package initialization
"""
from app.config.settings import settings
from app.database.base import init_db

__version__ = "2.0.0"
__all__ = ["settings", "init_db"]
