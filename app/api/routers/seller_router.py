from fastapi import APIRouter
from app.schemas.seller_schema import SellerCreate, SellerRead
from app.database.session import SessionDep
from app.services.seller_service import SellerService


router = APIRouter(prefix="/seller", tags=["seller"])


### Register Seller
@router.post("/signup", response_model=SellerRead)
async def register_seller(credentials: SellerCreate, session_db: SessionDep):

    return await SellerService(session_db).add(credentials)
