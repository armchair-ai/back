from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workflow_step import WorkflowStep
from app.repositories.workflow_step_repository import workflow_step_repository


class WorkflowStepService:
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_by_name(db, name=name)


    async def get_first_step(self, db: AsyncSession) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_first_step(db)

    async def get_next_step(self, db: AsyncSession, current_order: int) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_next_step(db, current_order=current_order)


workflow_step_service = WorkflowStepService()

