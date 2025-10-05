from datetime import datetime
from uuid import uuid4, UUID
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column


# -------------------------------------------------------
# ENUM
# -------------------------------------------------------
class ShipmentStatus(str, Enum):
    placed = "placed"
    out_for_delivery = "out_for_delivery"
    in_transit = "in_transit"
    delivered = "delivered"


# -------------------------------------------------------
# SHIPMENT MODEL
# -------------------------------------------------------
class Shipment(SQLModel, table=True):
    # __tablename__ = "shipment"
    # - Use `default_factory=uuid4` to auto-generate UUIDs in Python.
    # - Use `postgresql.UUID(as_uuid=True)` for correct Postgres mapping.
    id: UUID = Field(
        default_factory=uuid4,  # ✅ automatically generate a UUID
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    content: str
    weight: float = Field(le=25000)
    destination: str
    status: ShipmentStatus
    estimated_delivery: datetime

    # ✅ Keep this foreign key — just ensure the DB column exists via migration
    seller_id: UUID = Field(foreign_key="seller.id")

    # ✅ Relationship stays correct
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )


# -------------------------------------------------------
# SELLER MODEL
# -------------------------------------------------------
class Seller(SQLModel, table=True):
    # - Added `default_factory=uuid4` to auto-generate IDs
    # - Specified `postgresql.UUID(as_uuid=True)` for proper Postgres UUID type
    id: UUID = Field(
        default_factory=uuid4,  # ✅ automatically generate a UUID
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    name: str
    email: EmailStr
    password: str
    address: str

    # ✅ Relationship is fine as is
    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )


# -------------------------------------------------------
# DELIVERY PARTNER
# -------------------------------------------------------
class DeliveryPartner(SQLModel, table=True):

    id: UUID = Field(
        default_factory=uuid4,  # ✅ automatically generate a UUID
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    name: str
    email: EmailStr
    password: str
