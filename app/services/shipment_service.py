from datetime import datetime, timedelta
from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel import Session
from app.database.models import Shipment, ShipmentStatus, Seller
from app.schemas.shipment_schema import ShipmentCreate, ShipmentUpdate
from app.services.notification_service import NotificationService
from app.services.partner_service import DeliveryPartnerService
from fastapi import BackgroundTasks


class ShipmentService:
    def __init__(self, session_db: Session, background_tasks: BackgroundTasks) -> None:
        self.session_db = session_db
        self.notification_service = (
            NotificationService(background_tasks) if background_tasks else None
        )

    def get(self, id: UUID) -> Shipment | None:
        return self.session_db.get(Shipment, id)

    async def add(self, req_body: ShipmentCreate, seller_id: str) -> Shipment | None:

        partner_name = req_body.delivery_partner or "default"

        default_partner = DeliveryPartnerService(self.session_db).get_by_name(
            partner_name
        )

        if default_partner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Default delivery partner not found",
            )

        new_shipment = Shipment(
            **req_body.model_dump(exclude={"delivery_partner"}),
            status=ShipmentStatus.placed,
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=UUID(seller_id),
            delivery_partner_id=default_partner.id,
        )

        self.session_db.add(new_shipment)
        self.session_db.commit()
        self.session_db.refresh(new_shipment)

        self._notify(new_shipment)

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

        self._notify(shipment)

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

    def _notify(self, shipment: Shipment):
        match shipment.status:
            case ShipmentStatus.placed:
                self.notification_service.send_email(
                    recipients=[shipment.client_contact_email],
                    subject="Your order has been shipped",
                    body=f"Your Order with {shipment.seller.name} has been placed and ready to go",
                )
            case ShipmentStatus.out_for_delivery:
                self.notification_service.send_email(
                    recipients=[shipment.client_contact_email],
                    subject="Your order is on the way",
                    body=f"Your Order with {shipment.seller.name} has been picked up and on the way",
                )
