from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.database.redis import add_jti_to_blacklist
from app.schemas.seller_schema import SellerCreate, SellerRead
from app.database.session import SessionDep
from app.services.seller_service import SellerService
from app.auth.security import oauth2_scheme_seller
from app.utils import decode_access_token, generate_access_token
from app.database.models import Seller


router = APIRouter(prefix="/seller", tags=["Seller"])


### Register Seller
@router.post("/signup", response_model=SellerRead)
async def create_seller(credentials: SellerCreate, session_db: SessionDep):

    return SellerService(session_db).add(credentials)


### Login the Seller
@router.post("/login")
async def login_seller(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session_db: SessionDep
):
    token = SellerService(session_db).token(form_data.username, form_data.password)

    return {"access_token": token, "type": "jwt"}


@router.get("/dashboard")
async def get_dashboard(
    token: Annotated[str, Depends(oauth2_scheme_seller)], session_db: SessionDep
) -> Seller | None:

    user_data = decode_access_token(token)

    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Inavalid access token"
        )

    seller = session_db.get(Seller, UUID(user_data["user"]["id"]))

    return seller


@router.get("/logout")
async def logout_seller(token: str = Depends(oauth2_scheme_seller)):

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
