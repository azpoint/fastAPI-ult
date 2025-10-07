from uuid import UUID
from pydantic import BaseModel, EmailStr, ValidationInfo, field_validator


class DeliveryPartnerCreate(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[str]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    serviceable_zip_codes: list[str]
    max_handling_capacity: int


class DeliveryPartnerUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    serviceable_zip_codes: list[str] | None = None
    max_handling_capacity: int | None = None

    @field_validator("email", mode="before")
    def validate_email_or_empty(cls, v, info: ValidationInfo):
        if v in (None, ""):
            return None
        return v
