from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ModelNotFoundError
from app.repositories.message_repository import message_repository
from app.services.order_service import order_service
from app.schemas.message import MessageCreate
from app.models.message import Message

class MessageService:
    async def create_message_for_order(self, db: AsyncSession, order_id: int, message_in: MessageCreate) -> Message:
        # First ensure the order exists
        order = await order_service.get_order(db, order_id=order_id)
        if not order:
            raise ModelNotFoundError("Order not found")
        
        return await message_repository.create_with_order(db, obj_in=message_in, order_id=order_id)

message_service = MessageService()
