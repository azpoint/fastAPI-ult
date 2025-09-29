from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import Any
from fastapi import status, HTTPException
from app.database.session import SessionDep
from app.database.models import Shipment, ShipmentStatus
from app.schemas.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.services.shipment_service import ShipmentService


router = APIRouter(prefix="/shipment", tags=["Shipment"])

# # Get the latest shipment
# @router.get("/shipment/latest")
# async def get_latest_shipment() -> dict[str, Any]:
#     last_id = max(shipments.keys())

#     return {"id": last_id, **shipments[last_id]}


### Get shipment by ID
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, session_db: SessionDep):

    shipment = await ShipmentService(session_db).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# Create shipment
@router.post("/", response_model=Shipment)
async def submit_shipment(req_body: ShipmentCreate, session_db: SessionDep):

    shipment = await ShipmentService(session_db).add(req_body)

    return shipment


# Update shipment by field
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(id: int, req_body: ShipmentUpdate, session_db: SessionDep):

    shipment = await ShipmentService(session_db).update(req_body, id)

    return shipment


# Delete shipment by id
@router.delete("/")
async def delete_shipment_by_id(id: int, session_db: SessionDep) -> dict[str, Any]:

    await ShipmentService(session_db).delete(id)

    return {"detail": f"Shipment {id} deleted!"}
