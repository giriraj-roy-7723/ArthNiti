import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = os.getenv("DEBUG", "False") == "True"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []
    API_V1_STR = os.getenv("API_V1_STR", "/api/v1")