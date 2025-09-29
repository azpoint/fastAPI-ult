from pydantic import BaseModel, EmailStr


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class SellerRead(BaseModel):
    name: str
    email: EmailStr
