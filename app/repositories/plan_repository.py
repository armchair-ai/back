from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.plan import Plan
from app.schemas.plan import PlanCreate


class PlanRepository(BaseRepository[Plan, PlanCreate]):
    def __init__(self):
        super().__init__(Plan)

    async def get_by_message_id(self, db: AsyncSession, message_id: int) -> Optional[Plan]:
        result = await db.execute(
            select(self.model)
            .where(self.model.message_id == message_id)
            .order_by(self.model.id.desc())
        )
        return result.scalars().first()


plan_repository = PlanRepository()
