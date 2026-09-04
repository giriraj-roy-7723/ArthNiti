# ai_backend/ai_backend/app/__init__.py

from fastapi import FastAPI

app = FastAPI()

from .api import routes

app.include_router(routes.router)