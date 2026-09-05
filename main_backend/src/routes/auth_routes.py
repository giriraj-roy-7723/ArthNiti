from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer

from src.config.database import get_db
from src.middlewares.auth import verify_token
from src.models.auth_model import SignupRequest, LoginRequest
from src.controllers.auth_controller import signup_user, login_user, logout_user, get_my_profile

security = HTTPBearer()
router = APIRouter()


@router.post("/signup")
async def signup(
    data: SignupRequest,
    db: AsyncSession = Depends(get_db)
):
    return await signup_user(data, db)


@router.post("/login")
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    return await login_user(data, db)


@router.post("/logout")
async def logout(
    user_id: str = Depends(verify_token),
    credentials=Depends(security)
):
    token = credentials.credentials
    # print(token)
    return await logout_user(token)

@router.get("/me")
async def get_profile(
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):
    return await get_my_profile(user_id, db)
