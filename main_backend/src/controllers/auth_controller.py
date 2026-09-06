from fastapi import HTTPException

from src.schema.user import User, generate_unique_username
from src.schema.invite import Invite
from src.schema.buyer import Buyer
from src.schema.enterpreruner import Enterpreneur
from src.schema.government_officials import GovernmentOfficial

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.middlewares.auth import create_access_token
from src.utils.id_generator import generate_user_id
from src.utils.password import hash_password, verify_password
from src.services.storage_services import get_profile_image_url
from src.lib.redis_client import blacklist_token

from datetime import datetime, timezone

import os
from dotenv import load_dotenv

load_dotenv()

PROFILE_CACHE_TTL = 300  # 5 minutes

ROLE = {
    "enterpreneur": Enterpreneur,
    "buyer": Buyer,
    "government_official": GovernmentOfficial,
}


async def signup_user(data, db: AsyncSession):
    # Check if user already exists
    result = await db.execute(select(User).where(User.email == data.email))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user_id = generate_user_id()

    # Hash password and save user locally
    hashed_password = hash_password(data.password)

    username = await generate_unique_username(data.first_name, db)

    user = User(
        user_id=user_id,
        email=data.email,
        password=hashed_password,
        first_name=data.first_name,
        last_name=data.last_name,
        username=username,
        phone_number=data.phone_number,
        role=data.role,
        address=data.address,
        village=data.village,
        district=data.district,
        city=data.city,
        state=data.state,
        country=data.country,
        pincode=data.pincode,
    )

    db.add(user)

    await db.flush()  # Ensure user is assigned an ID if using autoincrement

    await db.commit()

    # admin will not be available in choice ,added check for safety
    if data.role == "government_official":
        result = await db.execute(
            select(Invite).where(Invite.email == data.email, Invite.role == data.role)
        )
        invite = result.scalar_one_or_none()
        if not invite:
            raise HTTPException(
                status_code=400,
                detail="No valid government official invite found for this email",
            )

        if invite.used:
            raise HTTPException(status_code=400, detail="Invite already used")

        if invite.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Invite expired")

        government_official = GovernmentOfficial(
            user_id=user.user_id,
            designation=data.designation,
            agency_type=data.agency_type,
            agency_name=data.agency_name,
        )
        db.add(government_official)
        await db.commit()

    elif data.role == "enterpreneur":
        enterpreneur = Enterpreneur(
            user_id=user.user_id,
        )

        db.add(enterpreneur)

        await db.commit()

    elif data.role == "buyer":
        investor = Buyer(
            user_id=user.user_id,
        )

        db.add(investor)

        await db.commit()

    else:
        raise HTTPException(status_code=400,message="Select a valid role among enterpreneur,buyer,government official")

    token = create_access_token({"user_id": user_id})

    return {
        "message": "Signup successful",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        },
        "access_token": token,
        "token_type": "bearer",
    }


async def login_user(data, db: AsyncSession):

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = user.user_id

    token = create_access_token({"user_id": user_id})

    return {
        "message": "Login successful",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "phone": user.phone_number,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
        },
        "access_token": token,
        "token_type": "bearer",
    }


async def logout_user(token: str):
    # Blacklist the token in Redis
    await blacklist_token(token)

    return {"message": "Logout successful"}


async def get_my_profile(user_id: str, db: AsyncSession):

    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_url = get_profile_image_url(user.profile_pic)

    role_result = await db.execute(
        select(ROLE[user.role]).where(ROLE[user.role].user_id == user_id)
    )
    role_info = role_result.scalar_one_or_none()

    role_info_dict = None

    if role_info:
        role_info_dict = {
            column.name: getattr(role_info, column.name)
            for column in role_info.__table__.columns
        }

        role_info_dict.pop("id", None)
        role_info_dict.pop("user_id", None)
        role_info_dict.pop("created_at", None)

    response = {
        "user_id": user.user_id,
        "email": user.email,
        "phone": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "address": user.address,
        "village": user.village,
        "district": user.district,
        "city": user.city,
        "state": user.state,
        "country": user.country,
        "pincode": user.pincode,
        "profile_image": image_url,
        "role_info": role_info_dict,
    }

    return response
