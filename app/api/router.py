from fastapi import APIRouter
from datetime import datetime, timedelta
from typing import Any
from fastapi import status, HTTPException
from app.database.session import SessionDep
from app.database.models import Shipment, ShipmentStatus
from app.schemas.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentUpdate


router = APIRouter()

# # Get the latest shipment
# @router.get("/shipment/latest")
# async def get_latest_shipment() -> dict[str, Any]:
#     last_id = max(shipments.keys())

#     return {"id": last_id, **shipments[last_id]}


### Get shipment by ID
@router.get("/shipment", response_model=ShipmentRead)
async def get_shipment_by_id(id: int, session_db: SessionDep):

    shipment = session_db.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# Create shipment
@router.post("/shipment", response_model=None)
async def submit_shipment(req_body: ShipmentCreate, session_db: SessionDep):

    new_shipment = Shipment(
        **req_body.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )

    session_db.add(new_shipment)
    session_db.commit()
    session_db.refresh(new_shipment)

    return {"id": new_shipment.id}


# Update shipment by field
@router.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, req_body: ShipmentUpdate, session_db: SessionDep):

    update = req_body.model_dump(exclude_none=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data provided to update"
        )

    shipment = session_db.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment not found"
        )

    shipment.sqlmodel_update(update)
    session_db.add(shipment)
    session_db.commit()
    session_db.refresh(shipment)

    return shipment


# Delete shipment by id
@router.delete("/shipment")
async def delete_shipment_by_id(id: int, session_db: SessionDep) -> dict[str, Any]:

    shipment = session_db.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Shipment {id} not found!"
        )

    session_db.delete(shipment)
    session_db.commit()

    return {"detail": f"Shipment {id} deleted!"}
