from pydantic import BaseModel, EmailStr


class DeliveryPartnerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    serviceable_zip_codes: list[str]
    max_handling_capacity: int


class DeliveryPartnerRead(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[str]
    max_handling_capacity: int


class DeliveryPartnerUpdate(BaseModel):
    name: str
    email: EmailStr
    serviceable_zip_codes: list[str]
    max_handling_capacity: int
