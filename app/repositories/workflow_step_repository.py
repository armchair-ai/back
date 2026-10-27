from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workflow_step import WorkflowStep
from app.repositories.base_repository import BaseRepository
from app.schemas.workflow_step import WorkflowStepCreate


class WorkflowStepRepository(BaseRepository[WorkflowStep, WorkflowStepCreate]):
    def __init__(self) -> None:
        super().__init__(WorkflowStep)

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[WorkflowStep]:
        result = await db.execute(
            select(self.model)
            .where(self.model.name == name)
        )
        return result.scalars().first()

    async def get_first_step(self, db: AsyncSession) -> Optional[WorkflowStep]:
        result = await db.execute(
            select(self.model)
            .order_by(self.model.order.asc())
            .limit(1)
        )
        return result.scalars().first()

    async def get_next_step(self, db: AsyncSession, current_order: int) -> Optional[WorkflowStep]:
        result = await db.execute(
            select(self.model)
            .where(self.model.order > current_order)
            .order_by(self.model.order.asc())
            .limit(1)
        )
        return result.scalars().first()


workflow_step_repository = WorkflowStepRepository()

