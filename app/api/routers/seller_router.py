from fastapi import APIRouter
from app.schemas.seller_schema import SellerCreate


router = APIRouter(prefix="/seller")


@router.post("/signup")
async def register_seller(seller: SellerCreate):
    pass
