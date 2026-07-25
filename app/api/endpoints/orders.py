from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreate, OrderResponse
from app.api.dependencies import get_db
from app.services.order_service import order_service

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    return await order_service.create_order(db, order_in=order_in)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await order_service.get_order(db, order_id=order_id)
