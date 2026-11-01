from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.workflow_step import WorkflowStep
from app.schemas.workflow_step import WorkflowStepListItemResponse
from app.repositories.workflow_step_repository import workflow_step_repository
from app.core.translator import trans


class WorkflowStepService:
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_by_name(db, name=name)

    async def get_first_step(self, db: AsyncSession) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_first_step(db)

    async def get_next_step(self, db: AsyncSession, current_order: int) -> Optional[WorkflowStep]:
        return await workflow_step_repository.get_next_step(db, current_order=current_order)

    async def get_all_ordered(self, db: AsyncSession) -> list[WorkflowStep]:
        return await workflow_step_repository.get_all_ordered(db)

    async def get_steps(
        self,
        db: AsyncSession,
        locale: str = "es",
    ) -> list[WorkflowStepListItemResponse]:
        steps = await workflow_step_repository.get_all_ordered(db)
        return [
            WorkflowStepListItemResponse(
                order=step.order,
                name=step.name,
                label=trans(f"workflow_steps.{step.name}", locale=locale),
            )
            for step in steps
        ]


workflow_step_service = WorkflowStepService()

