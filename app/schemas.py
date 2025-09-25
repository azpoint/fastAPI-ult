from datetime import datetime
from pydantic import BaseModel, Field
from app.database.models import ShipmentStatus


class ShipmentRead(BaseModel):
    content: str
    weight: float = Field(le=25000)
    status: ShipmentStatus
    destination: str
    estimated_delivery: datetime


class ShipmentCreate(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: str


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None = Field(default=None)
    estimated_delivery: datetime | None = Field(default=None)


### Base model inheritance version ###
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
