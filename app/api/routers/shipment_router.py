from typing import Annotated
from fastapi import APIRouter
from typing import Any
from fastapi import status, HTTPException, Depends
from app.database.session import SessionDep
from app.database.models import Shipment
from app.schemas.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.services.shipment_service import ShipmentService
from app.utils import decode_access_token
from app.auth.security import oauth2_scheme


router = APIRouter(prefix="/shipment", tags=["Shipment"])

# # Get the latest shipment
# @router.get("/shipment/latest")
# async def get_latest_shipment() -> dict[str, Any]:
#     last_id = max(shipments.keys())

#     return {"id": last_id, **shipments[last_id]}


### Get shipment by ID
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(
    token: Annotated[str, Depends(oauth2_scheme)], id: int, session_db: SessionDep
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = await ShipmentService(session_db).get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# Create shipment
@router.post("/", response_model=Shipment)
async def submit_shipment(
    token: Annotated[str, Depends(oauth2_scheme)],
    req_body: ShipmentCreate,
    session_db: SessionDep,
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = await ShipmentService(session_db).add(req_body)

    return shipment


# Update shipment by field
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    token: Annotated[str, Depends(oauth2_scheme)],
    id: int,
    req_body: ShipmentUpdate,
    session_db: SessionDep,
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = await ShipmentService(session_db).update(req_body, id)

    return shipment


# Delete shipment by id
@router.delete("/")
async def delete_shipment_by_id(
    token: Annotated[str, Depends(oauth2_scheme)], id: int, session_db: SessionDep
) -> dict[str, Any]:

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    await ShipmentService(session_db).delete(id)

    return {"detail": f"Shipment {id} deleted!"}
