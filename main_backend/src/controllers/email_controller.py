from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.models.email_request import InviteEmailRequest
from src.services.email_service import send_invite_email
from src.schema.invite import Invite


INVITE_EXPIRY_HOURS = 24


async def send_invitation(
    data: InviteEmailRequest,
    created_by: str,
    db: AsyncSession,
) -> dict[str, str]:

    expires_at = datetime.now(timezone.utc) + timedelta(
        hours=INVITE_EXPIRY_HOURS
    )

    invite = Invite(
        email=data.email,
        role=data.role,
        created_by=created_by,
        expires_at=expires_at,
        used=False,
    )

    db.add(invite)

    try:
        await db.commit()
        await db.refresh(invite)

    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Unable to create invitation",
        )

    try:
        await send_invite_email(
            data.email,
            data.invite_url,
        )

    except Exception as exc:
        # Remove the DB invitation if email sending failed
        await db.delete(invite)
        await db.commit()

        raise HTTPException(
            status_code=502,
            detail="Unable to send invitation email",
        ) from exc

    return {
        "message": "Invitation email sent successfully",
        "email": data.email,
        "invite_id": invite.id,
    }