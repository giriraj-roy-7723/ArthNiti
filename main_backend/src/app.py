import os
from fastapi import FastAPI
from src.config.database import engine, Base
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Tables before create:", Base.metadata.tables.keys())

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("Tables after create:", Base.metadata.tables.keys())

    yield


app = FastAPI(
    title="SKXYWTF Integration API",
    lifespan=lifespan,  # MUST be here
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# register routes
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
