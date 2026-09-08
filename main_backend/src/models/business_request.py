from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schema.business import BusinessStatus


class BusinessCreateRequest(BaseModel):
    business_name: str | None = None
    category: str | None = None
    description: str | None = None
    village: str | None = None
    district: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None

    margin_capital: float | None = Field(default=None, gt=0)
    pincode: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class BusinessResponse(BusinessCreateRequest):
    model_config = ConfigDict(from_attributes=True)

    id: str
    owner_id: str
    status: BusinessStatus
    created_at: datetime
    updated_at: datetime
