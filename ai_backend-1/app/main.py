from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

    setup_logging()

    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)