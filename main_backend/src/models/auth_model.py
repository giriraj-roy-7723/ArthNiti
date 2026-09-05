import phonenumbers
import enum
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from typing import Optional

class UserRole(str, enum.Enum): 
    entrepreneur = "entrepreneur" 
    buyer = "buyer" 
    government_official = "government_official"

class SignupRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "user@gmail.com"})

    password: str = Field(..., json_schema_extra={"example": "123456"})

    role: str = Field(default="user", json_schema_extra={"example": "buyer"})

    first_name: str = Field(..., json_schema_extra={"example": "John"})

    last_name: str = Field(..., json_schema_extra={"example": "Doe"})

    phone_number: str = Field(..., json_schema_extra={"example": "+914155552671"})

    address: str = Field(
        ...,
        json_schema_extra={"example": "12 Station Road"},
    )

    village: str = Field(
        ...,
        json_schema_extra={"example": "Madhyamgram"},
    )

    district: str = Field(
        ...,
        json_schema_extra={"example": "North 24 Parganas"},
    )

    city: str = Field(
        ...,
        json_schema_extra={"example": "Kolkata"},
    )

    state: str = Field(
        ...,
        json_schema_extra={"example": "West Bengal"},
    )

    country: str = Field(
        ...,
        json_schema_extra={"example": "India"},
    )

    pincode: str = Field(
        ...,
        json_schema_extra={"example": "700129"},
    )

    designation: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "District Manager"},
    )

    agency_type: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "sca"},
    )

    agency_name: Optional[str] = Field(
        default=None,
        json_schema_extra={"example": "State Council Agency"},
    )

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Name cannot be empty")

        if not all(char.isalpha() or char in " -'" for char in v):
            raise ValueError(
                "Name can contain only letters, spaces, hyphens and apostrophes"
            )

        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("email cannot be empty or whitespace")

        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Password cannot be empty or whitespace")

        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Role cannot be empty or whitespace")

        return v

    @field_validator(
        "address",
        "village",
        "district",
        "city",
        "state",
        "country",
    )
    @classmethod
    def validate_address_fields(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Address field cannot be empty or whitespace")

        return v

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, v: str) -> str:
        v = v.strip()

        if not v:
            raise ValueError("Pincode cannot be empty or whitespace")

        if not v.isdigit():
            raise ValueError("Pincode must contain only digits")

        if len(v) != 6:
            raise ValueError("Pincode must be exactly 6 digits")

        return v

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        try:
            number = phonenumbers.parse(v, None)

            if not phonenumbers.is_valid_number(number):
                raise ValueError("Invalid phone number")

            return phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164,
            )

        except Exception:
            raise ValueError("Invalid phone number format")

    @model_validator(mode="after")
    def validate_company_name(self):
        if self.role == "government_official" and (
            not self.designation or not self.designation.strip()
        ):
            raise ValueError(
                "designation is required for government_official role"
            )

        if self.role == "government_official" and (
            not self.agency_type or not self.agency_type.strip()
        ):
            raise ValueError(
                "agency type is required for government_official role"
            )

        if self.role == "government_official" and (
            not self.agency_name or not self.agency_name.strip()
        ):
            raise ValueError(
                "agency name is required for government_official role"
            )

        return self

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., json_schema_extra={"example": "user@gmail.com"})

    password: str

    @field_validator("email") 
    @classmethod
    def validate_email(cls, v: str) -> str: 
        if not v.strip(): 
            raise ValueError("email cannot be empty or whitespace") 
        return v
  
    @field_validator("password") 
    @classmethod
    def validate_password(cls, v: str) -> str: 
        if not v.strip(): 
            raise ValueError("Password cannot be empty or whitespace") 
        return v


from pydantic import BaseModel, model_validator
