from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from app.schemas.partner_schema import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from app.database.session import SessionDep
from app.services.partner_service import DeliveryPartnerService
from app.auth.security import oauth2_scheme_seller


router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Get Partner
@router.get("/signup", response_model=DeliveryPartnerRead)
async def get_partner(
    _token: Annotated[str, Depends(oauth2_scheme_seller)],
    email: EmailStr,
    session_db: SessionDep,
):
    service_response = DeliveryPartnerService(session_db).get_by_email(email)

    if service_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found"
        )

    return service_response


### Create Partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def create_partner(
    _token: Annotated[str, Depends(oauth2_scheme_seller)],
    req_body: DeliveryPartnerCreate,
    session_db: SessionDep,
):
    service_response = DeliveryPartnerService(session_db).add(req_body)

    if service_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found"
        )

    return service_response


### Update Delivery Partner
@router.patch("/{current_email}")
async def update_delivery_partner(
    _token: Annotated[str, Depends(oauth2_scheme_seller)],
    req_body: DeliveryPartnerUpdate,
    current_email: EmailStr,
    session_db: SessionDep,
):

    service_response = DeliveryPartnerService(session_db).update(
        req_body, current_email
    )

    if service_response is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Partner not found"
        )

    return service_response


@router.delete("/{uuid}")
async def delete_delivery_partner(
    _token: Annotated[str, Depends(oauth2_scheme_seller)],
    uuid: UUID,
    session_db: SessionDep,
):
    result = DeliveryPartnerService(session_db).delete(uuid)

    if not result:
        raise HTTPException(status_code=404, detail="Partner not found")

    return JSONResponse(content=result, status_code=status.HTTP_202_ACCEPTED)
