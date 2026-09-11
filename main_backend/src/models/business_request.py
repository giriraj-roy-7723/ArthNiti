from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr, HttpUrl
from typing import Optional

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


class BusinessImagesUpdateRequest(BaseModel):
    image_urls: list[HttpUrl] = Field(default_factory=list, max_length=20)


class BusinessImagesResponse(BaseModel):
    business_id: str
    image_urls: list[str] = Field(default_factory=list)


class BusinessOwnerContactResponse(BaseModel):
    business_id: str
    owner_id: str
    owner_name: str | None = None
    email: EmailStr | str | None = None
    phone_number: str | None = None

    class Config:
        from_attributes = True


class BusinessUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, description="Business name")
    description: Optional[str] = Field(None, description="Business description")
    village: Optional[str] = Field(None, description="Village name")
    district: Optional[str] = Field(None, description="District name")
    city: Optional[str] = Field(None, description="City name")
    state: Optional[str] = Field(None, description="State name")
    country: Optional[str] = Field(None, description="Country name")
    margin_capital: Optional[float] = Field(None, description="Margin capital amount")
    pincode: Optional[str] = Field(None, description="Postal code")
    latitude: Optional[float] = Field(None, description="Latitude coordinate")
    longitude: Optional[float] = Field(None, description="Longitude coordinate")
