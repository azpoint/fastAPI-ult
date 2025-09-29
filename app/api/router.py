from fastapi import APIRouter
from app.api.routers import shipment_router, seller_router

master_router = APIRouter()

master_router.include_router(shipment_router.router)
master_router.include_router(seller_router.router)
