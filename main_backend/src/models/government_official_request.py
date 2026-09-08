from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.schema.government_officials import RoleType


class GovernmentOfficialUpdateRequest(BaseModel):
    designation: str | None = None
    agency_name: str | None = None
    agency_address: str | None = None
    agency_city: str | None = None
    agency_state: str | None = None
    agency_country: str | None = None
    agency_type: RoleType | None = None
    agency_pincode: str | None = None


class GovernmentOfficialResponse(GovernmentOfficialUpdateRequest):
    model_config = ConfigDict(from_attributes=True)
    id: str
    user_id: str
    created_at: datetime
