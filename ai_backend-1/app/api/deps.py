from fastapi import Depends
from app.core.config import get_settings

def get_db():
    # Dependency to get the database session
    pass

def get_settings_dependency():
    # Dependency to get application settings
    return get_settings()