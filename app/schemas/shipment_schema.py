from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.database.models import Seller, ShipmentStatus


class ShipmentRead(BaseModel):
    id: UUID
    content: str
    weight: float = Field(le=25000)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime
    seller: Seller


class ShipmentCreate(BaseModel):
    content: str
    weight: float = Field(le=25000)
    destination: str


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)


### Base model class version ###
# class BaseShipment(BaseModel):
#     content: str
#     weight: float = Field(le=25)
#     destination: str


# class ShipmentRead(BaseShipment):
#     status: ShipmentStatus


# class ShipmentCreate(BaseShipment):
#     pass


# class ShipmentUpdate(BaseModel):
#     status: ShipmentStatus
