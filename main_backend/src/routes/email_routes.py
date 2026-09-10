from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import get_db

from src.controllers.email_controller import send_invitation
from src.middlewares.auth import verify_token
from src.middlewares.role import require_admin
from src.models.email_request import InviteEmailRequest

router = APIRouter()


@router.post("/invite", status_code=status.HTTP_200_OK)
async def send_invitation_email(
    data: InviteEmailRequest,
    admin: str = Depends(require_admin),
    db: AsyncSession = Depends(get_db),
):
    return await send_invitation(data, admin.user_id, db)


