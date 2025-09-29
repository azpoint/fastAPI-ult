from datetime import datetime
from enum import Enum
from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = "placed"
    out_for_delivery = "out_for_delivery"
    in_transit = "in_transit"
    delivered = "delivered"


class Shipment(SQLModel, table=True):
    # __tablename__ = "shipment"

    id: int | None = Field(default=None, primary_key=True)
    content: str
    weight: float = Field(le=25000)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime
