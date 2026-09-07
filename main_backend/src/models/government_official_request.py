from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schema.government_officials import RoleType


class GovernmentOfficialCreateRequest(BaseModel):
    designation: dict[str, str]
    agency_name: dict[str, str]
    agency_address: dict[str, str] | None = None
    agency_city: dict[str, str] | None = None
    agency_state: dict[str, str] | None = None
    agency_country: dict[str, str] | None = None
    agency_type: RoleType
    agency_pincode: str | None = None


class GovernmentOfficialResponse(GovernmentOfficialCreateRequest):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    created_at: datetime