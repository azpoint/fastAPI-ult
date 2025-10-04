from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session
from app.database.models import Shipment, ShipmentStatus, Seller
from app.schemas.shipment_schema import ShipmentCreate, ShipmentUpdate


class ShipmentService:
    def __init__(self, session_db: Session) -> None:
        self.session_db = session_db

    async def get(self, id: UUID) -> Shipment | None:
        return self.session_db.get(Shipment, id)

    async def add(
        self, shipment_create: ShipmentCreate, seller_id: str
    ) -> Shipment | None:

        new_shipment = Shipment(
            **shipment_create.model_dump(),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=UUID(seller_id),
        )

        self.session_db.add(new_shipment)
        self.session_db.commit()
        self.session_db.refresh(new_shipment)

        return new_shipment

    async def update(
        self, shipment_update: ShipmentUpdate, shipment_id: UUID
    ) -> Shipment | None:

        update = shipment_update.model_dump(exclude_none=True)

        if not update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No data provided to update",
            )

        shipment = self.session_db.get(Shipment, shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
            )

        shipment.sqlmodel_update(update)
        self.session_db.add(shipment)
        self.session_db.commit()
        self.session_db.refresh(shipment)

        return shipment

    async def delete(self, shipment_id: UUID) -> None:
        shipment = self.session_db.get(Shipment, shipment_id)

        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment {str(shipment_id)} not found!",
            )

        self.session_db.delete(shipment)
        self.session_db.commit()
