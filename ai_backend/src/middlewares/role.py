from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.middlewares.auth import verify_token
from src.config.database import get_db
from src.schema.user import User
from src.schema.enterpreneur import Enterpreneur


async def require_admin(
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    return user


async def require_enterpreneur(
    user_id: str = Depends(verify_token),
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(User).where(User.user_id == user_id)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if user.role != "enterpreneur":
        raise HTTPException(status_code=403, detail="You're not an enterpreneur")

    result = await db.execute(
        select(Enterpreneur).where(Enterpreneur.user_id == user_id)
    )
    employer = result.scalar_one_or_none()

    if not employer:
        raise HTTPException(status_code=404, detail="enterpreneur not found")
    
    return employer