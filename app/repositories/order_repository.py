from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.repositories.base_repository import BaseRepository
from app.models.order import Order
from app.schemas.order import OrderCreate
from typing import Optional

class OrderRepository(BaseRepository[Order, OrderCreate]):
    def __init__(self):
        super().__init__(Order)
        
    async def get_with_messages(self, db: AsyncSession, id: int) -> Optional[Order]:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.messages)).filter(self.model.id == id)
        )
        return result.scalars().first()

    async def get_all_with_messages(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Order]:
        result = await db.execute(
            select(self.model).options(selectinload(self.model.messages)).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

order_repository = OrderRepository()
