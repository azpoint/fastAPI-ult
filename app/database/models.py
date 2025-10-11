from datetime import date, datetime
from uuid import uuid4, UUID
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects import postgresql
from sqlalchemy import ARRAY, String, Column


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
    __tablename__ = "shipment"  # type: ignore

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    client_contact_email: EmailStr | None
    client_contact_phone: str | None
    content: str = Field(min_length=1, max_length=255)
    weight: float = Field(gt=0, le=25000)
    destination: str = Field(min_length=1, max_length=255)
    status: ShipmentStatus
    estimated_delivery: datetime

    seller_id: UUID = Field(foreign_key="seller.id")
    seller: "Seller" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )

    delivery_partner_id: UUID = Field(foreign_key="delivery_partner.id")

    delivery_partner: "DeliveryPartner" = Relationship(
        back_populates="shipments", sa_relationship_kwargs={"lazy": "selectin"}
    )


# -------------------------------------------------------
# SELLER MODEL
# -------------------------------------------------------
class Seller(SQLModel, table=True):
    __tablename__ = "seller"  # type: ignore

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    name: str
    email: EmailStr = Field(postgresql.VARCHAR, unique=True, nullable=False, index=True)
    password: str
    address: str

    shipments: list[Shipment] = Relationship(
        back_populates="seller", sa_relationship_kwargs={"lazy": "selectin"}
    )


# -------------------------------------------------------
# DELIVERY PARTNER
# -------------------------------------------------------
class DeliveryPartner(SQLModel, table=True):
    __tablename__ = "delivery_partner"  # type: ignore

    id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(postgresql.UUID(as_uuid=True), primary_key=True),
    )

    created_at: datetime = Field(
        sa_column=Column(
            postgresql.TIMESTAMP,
            default=datetime.now,
        )
    )

    name: str
    email: EmailStr

    serviceable_zip_codes: list[str] = Field(sa_column=Column(ARRAY(String)))
    max_handling_capacity: int

    shipments: list[Shipment] = Relationship(
        back_populates="delivery_partner", sa_relationship_kwargs={"lazy": "selectin"}
    )
