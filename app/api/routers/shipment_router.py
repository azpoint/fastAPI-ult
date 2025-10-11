from typing import Annotated
from uuid import UUID
from fastapi import APIRouter
from typing import Any
from fastapi import status, HTTPException, Depends
from app.database.session import SessionDep
from app.database.models import Shipment
from app.schemas.shipment_schema import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.services.shipment_service import ShipmentService
from app.utils import decode_access_token
from app.auth.security import oauth2_scheme_seller
from fastapi import BackgroundTasks


router = APIRouter(prefix="/shipment", tags=["Shipment"])


### Get shipment by ID
@router.get("/", response_model=ShipmentRead)
async def get_shipment_by_id(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
    id: UUID,
    session_db: SessionDep,
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = ShipmentService(session_db).get(id)  # type: ignore

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


### Create shipment
@router.post("/", response_model=Shipment)
async def create_shipment(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
    req_body: ShipmentCreate,
    session_db: SessionDep,
    background_tasks: BackgroundTasks,
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = await ShipmentService(session_db, background_tasks).add(req_body, user["user"]["id"])  # type: ignore

    return shipment


### Update shipment by field
@router.patch("/", response_model=ShipmentRead)
async def update_shipment(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
    shipment_id: UUID,
    req_body: ShipmentUpdate,
    session_db: SessionDep,
    background_tasks: BackgroundTasks,
):

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    shipment = await ShipmentService(session_db, background_tasks).update(
        req_body, shipment_id
    )

    return shipment


### Delete shipment by id
@router.delete("/")
async def delete_shipment_by_id(
    token: Annotated[str, Depends(oauth2_scheme_seller)],
    shipment_id: UUID,
    session_db: SessionDep,
) -> dict[str, Any]:

    user = decode_access_token(token)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    await ShipmentService(session_db).delete(shipment_id)

    return {"detail": f"Shipment {str(shipment_id)} deleted!"}
