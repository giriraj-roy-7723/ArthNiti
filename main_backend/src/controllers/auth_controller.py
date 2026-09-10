import asyncio

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.lib.redis_client import redis
from src.schema.user import User, UserRole, generate_unique_username
from src.schema.invite import Invite
from src.schema.buyer import Buyer
from src.schema.enterpreneur import Enterpreneur
from src.schema.government_officials import GovernmentOfficial

from src.middlewares.auth import create_access_token
from src.utils.id_generator import generate_user_id
from src.utils.password import hash_password, verify_password
from src.services.storage_services import get_profile_image_url
from src.lib.redis_client import blacklist_token

from src.controllers.government_official_controller import (
    get_government_official,
)
from src.models.auth_model import UserUpdateRequest

from src.utils.translator_utils import translate_entry

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


LANG_NORMALIZER = {
    "english": "en",
    "en": "en",
    "eng": "en",
    "bengali": "bn",
    "bng": "bn",
    "bn": "bn",
    "hindi": "hi",
    "hin": "hi",
    "hi": "hi",
}


USER_MULTILINGUAL_FIELDS = [
    "first_name",
    "last_name",
    "address",
    "village",
    "district",
    "city",
    "state",
    "country",
]



def get_user_source_language(
    user: User,
    target_language: str,
) -> str | None:
    """
    Find a language that already exists in the user's database fields.

    English is NOT assumed to exist.
    """

    available_languages = set()

    for field in USER_MULTILINGUAL_FIELDS:
        value = getattr(user, field, None) or {}

        if isinstance(value, dict):
            available_languages.update(value.keys())

    # Prefer a language different from the requested language
    for language in available_languages:
        if language != target_language:
            return language

    # Fallback if the requested language is the only language available
    if target_language in available_languages:
        return target_language

    return None


async def ensure_user_language(
    user: User,
    target_language: str,
    db: AsyncSession,
):
    """
    Make sure all multilingual user fields contain the requested language.

    If even one field is missing, translate all available fields in one call.
    """

    translation_missing = any(
        target_language not in (getattr(user, field, None) or {})
        for field in USER_MULTILINGUAL_FIELDS
    )

    if not translation_missing:
        return

    # Find a language that already exists in DB
    source_language = get_user_source_language(
        user=user,
        target_language=target_language,
    )

    if not source_language:
        raise HTTPException(
            status_code=400,
            detail="No source language available for user translation",
        )

    # Build source data
    source_entry = {}

    for field in USER_MULTILINGUAL_FIELDS:
        value = getattr(user, field, None) or {}

        source_value = value.get(source_language)

        if source_value is not None:
            source_entry[field] = source_value

    if not source_entry:
        raise HTTPException(
            status_code=400,
            detail="No user data available for translation",
        )

    # Translate all fields in one call
    translated_entry = await asyncio.to_thread(
        translate_entry,
        entry=source_entry,
        target_language=target_language,
        source_language=source_language,
    )

    # Store translations
    for field in USER_MULTILINGUAL_FIELDS:
        translated_value = translated_entry.get(field)

        if translated_value is None:
            continue

        current_value = getattr(user, field, None) or {}

        updated_value = dict(current_value)
        updated_value[target_language] = translated_value

        setattr(
            user,
            field,
            updated_value,
        )

    await db.commit()
    await db.refresh(user)

async def signup_user(data, language: str, db: AsyncSession):
    # Check if user already exists
    verified = await redis.get(f"otp_verified:{data.email}")
    if not verified:
        raise HTTPException(status_code=400, detail="Email not verified")

    lang_code = LANG_NORMALIZER[language.strip().lower()]

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
        first_name={lang_code: data.first_name},
        last_name={lang_code: data.last_name},
        username=username,
        phone_number=data.phone_number,
        role=data.role,
        address={lang_code: data.address},
        village={lang_code: data.village},
        district={lang_code: data.district},
        city={lang_code: data.city},
        state={lang_code: data.state},
        country={lang_code: data.country},
        pincode=data.pincode,
        email_verified=True,
    )

    db.add(user)

    await db.flush()  # Ensure user is assigned an ID if using autoincrement

    await db.commit()

    # admin will not be available in choice ,added check for safety
    if data.role == "government":
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
            designation={lang_code: data.designation},
            agency_type=data.agency_type,
            agency_name={lang_code: data.agency_name},
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
        raise HTTPException(
            status_code=400,
            message="Select a valid role among enterpreneur,buyer,government official",
        )

    token = create_access_token({"user_id": user_id})

    return {
        "message": "Signup successful",
        "user": {
            "user_id": user.user_id,
            "email": user.email,
            "first_name": user.first_name.get(lang_code, ""),
            "last_name": user.last_name.get(lang_code, ""),
            "role": user.role,
        },
        "access_token": token,
        "token_type": "bearer",
    }


async def login_user(data, language: str, db: AsyncSession):

    lang_code = LANG_NORMALIZER[language.strip().lower()]

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
            "first_name": user.first_name.get(lang_code, ""),
            "last_name": user.last_name.get(lang_code, ""),
            "role": user.role,
        },
        "access_token": token,
        "token_type": "bearer",
    }


async def logout_user(token: str):
    # Blacklist the token in Redis
    await blacklist_token(token)

    return {"message": "Logout successful"}


async def get_my_profile(
    user_id: str,
    language: str,
    db: AsyncSession,
):

    lang_code = LANG_NORMALIZER.get(language.strip().lower())

    if not lang_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}",
        )

    # ---------------------------------------------------------
    # Get user
    # ---------------------------------------------------------

    result = await db.execute(select(User).where(User.user_id == user_id))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    # ---------------------------------------------------------
    # Ensure requested language exists
    # ---------------------------------------------------------

    await ensure_user_language(
        user=user,
        target_language=lang_code,
        db=db,
    )

    # ---------------------------------------------------------
    # Profile image
    # ---------------------------------------------------------

    image_url = get_profile_image_url(user.profile_pic)

    # ---------------------------------------------------------
    # Role-specific information
    # ---------------------------------------------------------

    role_result = {}

    if user.role == UserRole.government:
        role_result = await get_government_official(
            user_id=user_id,
            language=language,
            db=db,
        )

    # ---------------------------------------------------------
    # Return requested language only
    # ---------------------------------------------------------

    response = {
        "user_id": user.user_id,
        "email": user.email,
        "phone": user.phone_number,
        "first_name": (user.first_name or {}).get(lang_code, ""),
        "last_name": (user.last_name or {}).get(lang_code, ""),
        "role": user.role,
        "address": (user.address or {}).get(lang_code, ""),
        "village": (user.village or {}).get(lang_code, ""),
        "district": (user.district or {}).get(lang_code, ""),
        "city": (user.city or {}).get(lang_code, ""),
        "state": (user.state or {}).get(lang_code, ""),
        "country": (user.country or {}).get(lang_code, ""),
        "pincode": user.pincode,
        "profile_image": image_url,
        "role_info": role_result,
    }

    return response


from sqlalchemy.exc import IntegrityError

async def update_my_profile(
    data: UserUpdateRequest,
    language: str,
    user_id: str,
    db: AsyncSession,
) -> User:

    lang_code = LANG_NORMALIZER.get(language.strip().lower())

    if not lang_code:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}",
        )

    # Get existing user
    result = await db.execute(select(User).where(User.user_id == user_id))

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    multilingual_fields = [
        "first_name",
        "last_name",
        "address",
        "village",
        "district",
        "city",
        "state",
        "country",
    ]

    # ---------------------------------------------------------
    # Check whether any multilingual field is being updated
    # ---------------------------------------------------------

    multilingual_updates = {
        "first_name": data.first_name,
        "last_name": data.last_name,
        "address": data.address,
        "village": data.village,
        "district": data.district,
        "city": data.city,
        "state": data.state,
        "country": data.country,
    }

    has_multilingual_update = any(
        value is not None for value in multilingual_updates.values()
    )

    if has_multilingual_update:
        # -----------------------------------------------------
        # Get the currently stored language
        # -----------------------------------------------------

        source_language = None

        for field in multilingual_fields:
            value = getattr(user, field, None) or {}

            if isinstance(value, dict) and value:
                source_language = next(iter(value.keys()))
                break

        # -----------------------------------------------------
        # Build the complete profile in the new language
        # -----------------------------------------------------

        translated_entry = {}

        # If existing data exists in another language,
        # use it as the source.
        if source_language and source_language != lang_code:
            source_entry = {}

            for field in multilingual_fields:
                value = getattr(user, field, None) or {}

                if isinstance(value, dict):
                    source_value = value.get(source_language)

                    if source_value is not None:
                        source_entry[field] = source_value

            if source_entry:
                translated_entry = await asyncio.to_thread(
                    translate_entry,
                    entry=source_entry,
                    target_language=lang_code,
                    source_language=source_language,
                )

        # -----------------------------------------------------
        # Apply fields explicitly supplied in PATCH
        # -----------------------------------------------------

        for field, value in multilingual_updates.items():
            if value is not None:
                translated_entry[field] = value

        # -----------------------------------------------------
        # Store ONLY the requested language
        # -----------------------------------------------------

        for field in multilingual_fields:
            value = translated_entry.get(field)

            if value is not None:
                setattr(
                    user,
                    field,
                    {lang_code: value},
                )

    # ---------------------------------------------------------
    # Update non-translated fields
    # ---------------------------------------------------------

    if data.phone_number is not None:
        user.phone_number = data.phone_number

    if data.pincode is not None:
        user.pincode = data.pincode

    if data.profile_pic is not None:
        user.profile_pic = data.profile_pic

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    try:
        await db.commit()
        await db.refresh(user)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Unable to update user profile",
        )

    return user