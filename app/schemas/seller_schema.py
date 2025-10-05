from pydantic import BaseModel, EmailStr


class SellerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    address: str


class SellerRead(BaseModel):
    name: str
    email: EmailStr
    address: str
