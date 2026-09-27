from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ModelNotFoundError
from app.core.event_dispatcher import event_dispatcher
from app.events.message import MessageCreatedEvent
from app.repositories.message_repository import message_repository
from app.services.order_service import order_service
from app.schemas.message import MessageCreate
from app.models.message import Message

class MessageService:
    async def create_message_for_order(self, db: AsyncSession, order_id: int, message_in: MessageCreate) -> Message:
        order = await order_service.get_order(db, order_id=order_id)
        if not order:
            raise ModelNotFoundError("Order not found")
        
        message = await message_repository.create_with_order(db, obj_in=message_in, order_id=order_id)
        event = MessageCreatedEvent(id=message.id)
        await event_dispatcher.dispatch(event)
        return message



message_service = MessageService()
