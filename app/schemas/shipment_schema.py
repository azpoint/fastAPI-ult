from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from app.database.models import Seller, ShipmentStatus, DeliveryPartner


class ShipmentRead(BaseModel):
    id: UUID
    content: str
    weight: float = Field(le=25000)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime
    seller: Seller
    delivery_partner: DeliveryPartner


class ShipmentCreate(BaseModel):
    content: str
    weight: float = Field(le=25000)
    destination: str
    delivery_partner: str


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = None
    estimated_delivery: datetime | None = None


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
