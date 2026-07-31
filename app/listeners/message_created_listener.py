import logging
from pydantic import BaseModel
from app.events.message import MessageCreatedEvent
from app.core.database import AsyncSessionLocal
from app.repositories.message_repository import message_repository
from app.core.event_dispatcher import event_dispatcher

logger = logging.getLogger(__name__)


async def message_created_listener(event: BaseModel) -> None:
    if isinstance(event, MessageCreatedEvent):
        logger.info(f"[MessageCreatedListener] Event received for message ID: {event.id}, Order ID: {event.order_id}")
        async with AsyncSessionLocal() as db:
            message = await message_repository.get(db, id=event.id)
            if message:
                logger.info(f"[MessageCreatedListener] Found message in DB. Text: '{message.text}'")
            else:
                logger.warning(f"[MessageCreatedListener] Message with ID {event.id} not found in DB.")


event_dispatcher.register(message_created_listener)
