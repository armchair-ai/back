from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.message import MessageCreate, MessageResponse
from app.api.dependencies import get_db
from app.services.message_service import message_service

router = APIRouter()

@router.post("/orders/{order_id}/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    message_in: MessageCreate,
    order_id: int = Path(..., description="The ID of the order to add the message to"),
    db: AsyncSession = Depends(get_db)
):
    return await message_service.create_message_for_order(db, order_id=order_id, message_in=message_in)
