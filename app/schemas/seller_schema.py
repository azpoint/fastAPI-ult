from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_validator


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., min_length=5)
    address: str

    @field_validator("password")
    def password_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Password must not be empty.")
        return v


class SellerRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    address: str
