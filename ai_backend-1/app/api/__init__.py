# ai_backend/ai_backend/app/api/__init__.py

from fastapi import APIRouter

router = APIRouter()

from .routes import *  # Import all routes to register them with the router
