from datetime import datetime, timezone
from typing import Any, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message_workflow_step import MessageWorkflowStep
from app.repositories.base_repository import BaseRepository


class MessageWorkflowStepRepository(BaseRepository[MessageWorkflowStep, Any]):
    def __init__(self) -> None:
        super().__init__(MessageWorkflowStep)

    async def get_with_step(self, db: AsyncSession, id: int) -> MessageWorkflowStep:
        result = await db.execute(
            select(self.model)
            .options(selectinload(self.model.workflow_step))
            .where(self.model.id == id)
        )
        return result.scalars().first()

    async def create_step(
        self,
        db: AsyncSession,
        *,
        message_id: int,
        workflow_step_id: int,
        status: str = "running",
        started_at: Optional[datetime] = None,
        finished_at: Optional[datetime] = None,
    ) -> MessageWorkflowStep:
        db_obj = self.model(
            message_id=message_id,
            workflow_step_id=workflow_step_id,
            status=status,
            started_at=started_at,
            finished_at=finished_at,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def mark_finished(
        self,
        db: AsyncSession,
        *,
        id: int,
        status: str = "completed",
        finished_at: Optional[datetime] = None,
    ) -> MessageWorkflowStep:
        step = await self.get(db, id=id)
        step.status = status
        step.finished_at = finished_at or datetime.now(timezone.utc)
        db.add(step)
        await db.commit()
        await db.refresh(step)
        return step

    async def mark_failed(
        self,
        db: AsyncSession,
        *,
        id: int,
    ) -> MessageWorkflowStep:
        step = await self.get(db, id=id)
        step.status = "failed"
        db.add(step)
        await db.commit()
        await db.refresh(step)
        return step


message_workflow_step_repository = MessageWorkflowStepRepository()

