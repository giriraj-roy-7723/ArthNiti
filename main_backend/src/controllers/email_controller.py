from fastapi import HTTPException

from src.models.email_request import InviteEmailRequest
from src.services.email_service import send_invite_email


async def send_invitation(data: InviteEmailRequest) -> dict[str, str]:
    try:
        await send_invite_email(data.email, data.invite_url)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Unable to send invitation email",
        ) from exc

    return {"message": "Invitation email sent successfully", "email": data.email}