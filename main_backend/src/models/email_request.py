from pydantic import BaseModel, Field


class InviteEmailRequest(BaseModel):
    email: str = Field(min_length=3)
    invite_url: str = Field(min_length=1)