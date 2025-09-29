from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.seller_schema import SellerCreate, SellerRead
from app.database.session import SessionDep
from app.services.seller_service import SellerService


router = APIRouter(prefix="/seller", tags=["seller"])


### Register Seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(credentials: SellerCreate, session_db: SessionDep):

    return await SellerService(session_db).add(credentials)


### Login the Seller
@router.post("/login")
async def login_seller(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session_db: SessionDep
):
    token = SellerService(session_db).login(form_data.username, form_data.password)

    return {"access_token": token, "type": "jwt"}
