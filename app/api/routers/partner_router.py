from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database.redis import add_jti_to_blacklist
from app.schemas.partner_schema import (
    DeliveryPartnerCreate,
    DeliveryPartnerRead,
    DeliveryPartnerUpdate,
)
from app.database.session import SessionDep
from app.services.partner_service import DeliveryPartnerService
from app.auth.security import oauth2_scheme_partner
from app.utils import decode_access_token
from app.database.models import DeliveryPartner


router = APIRouter(prefix="/partner", tags=["Delivery Partner"])


### Create Partner
@router.post("/signup", response_model=DeliveryPartnerRead)
async def create_partner(req_body: DeliveryPartnerCreate, session_db: SessionDep):

    return DeliveryPartnerService(session_db).add(req_body)


### Login the Partner
@router.post("/login")
async def login_partner(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session_db: SessionDep
):
    token = DeliveryPartnerService(session_db).token(
        form_data.username, form_data.password
    )

    return {"access_token": token, "type": "jwt"}


@router.get("/dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme_partner)], session_db: SessionDep
) -> DeliveryPartner | None:

    user_data = decode_access_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    partner = session_db.get(DeliveryPartner, UUID(user_data["user"]["id"]))

    return partner


### Update Delivery Partner
@router.patch("/")
async def update_delivery_partner(
    token: Annotated[str, Depends(oauth2_scheme_partner)],
    req_body: DeliveryPartnerUpdate,
    session_db: SessionDep,
):
    return DeliveryPartnerService(session_db).update(req_body, token)


### Logout Partner
@router.get("/logout")
async def logout_partner(token: str = Depends(oauth2_scheme_partner)):

    user_data = decode_access_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    jti = user_data.get("jti")

    if jti is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Missing jti in token"
        )

    await add_jti_to_blacklist(jti)

    return {"detail": "Successfully logged out"}
