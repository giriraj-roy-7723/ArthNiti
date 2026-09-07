from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schema.business import BusinessStatus


class BusinessCreateRequest(BaseModel):
    business_name: dict[str, str]
    category: dict[str, str]
    description: dict[str, str] | None = None
    village: dict[str, str] | None = None
    district: dict[str, str]
    city: dict[str, str] | None = None
    state: dict[str, str]
    country: dict[str, str]
    margin_capital: float = Field(gt=0)
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