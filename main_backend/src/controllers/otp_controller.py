import random

from fastapi import HTTPException

from src.services.email_service import send_otp_email
from src.lib.redis_client import redis


OTP_TTL_SECONDS = 300  # 5 minutes
OTP_VERIFIED_TTL_SECONDS = 600  # 10 minutes, gives signup form time to submit


async def send_email_otp(email: str) -> dict[str, str]:

    otp = str(random.randint(100000, 999999))

    await redis.set(f"otp:{email}", otp, ex=OTP_TTL_SECONDS)

    try:
        await send_otp_email(email, otp)

    except Exception as exc:
        await redis.delete(f"otp:{email}")

        raise HTTPException(
            status_code=502,
            detail="Unable to send verification email",
        ) from exc

    return {
        "message": "OTP sent successfully",
        "email": email,
    }


async def verify_email_otp(email: str, otp: str) -> dict[str, str]:

    stored_otp = await redis.get(f"otp:{email}")

    if not stored_otp:
        raise HTTPException(
            status_code=400,
            detail="OTP expired or not found, please request a new one",
        )

    if stored_otp != otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP",
        )

    await redis.delete(f"otp:{email}")

    await redis.set(
        f"otp_verified:{email}",
        "true",
        ex=OTP_VERIFIED_TTL_SECONDS,
    )

    return {
        "message": "Email verified successfully",
        "email": email,
    }