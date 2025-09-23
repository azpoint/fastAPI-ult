from pydantic import BaseModel, Field
from enum import Enum


class ShipmentStatus(str, Enum):
    placed = "placed"
    in_transit = "in_transit"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"


class ShipmentRead(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: str
    status: ShipmentStatus


class ShipmentCreate(BaseModel):
    content: str
    weight: float = Field(le=25)
    destination: str


class ShipmentUpdate(BaseModel):
    status: ShipmentStatus


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
