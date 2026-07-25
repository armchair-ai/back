from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.message import Message
from app.schemas.message import MessageCreate

class MessageRepository(BaseRepository[Message, MessageCreate]):
    def __init__(self):
        super().__init__(Message)

    async def create_with_order(self, db: AsyncSession, *, obj_in: MessageCreate, order_id: int) -> Message:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data, order_id=order_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

message_repository = MessageRepository()
