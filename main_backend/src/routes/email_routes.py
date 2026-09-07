from fastapi import APIRouter, Depends, status

from src.controllers.email_controller import send_invitation
from src.middlewares.auth import verify_token
from src.models.email_request import InviteEmailRequest

router = APIRouter()


@router.post("/invite", status_code=status.HTTP_200_OK)
async def send_invitation_email(
    data: InviteEmailRequest,
    user_id: str = Depends(verify_token),
):
    return await send_invitation(data)