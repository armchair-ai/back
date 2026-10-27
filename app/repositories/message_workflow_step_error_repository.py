from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message_workflow_step_error import MessageWorkflowStepError
from app.repositories.base_repository import BaseRepository
from app.schemas.message_workflow_step_error import MessageWorkflowStepErrorCreate


class MessageWorkflowStepErrorRepository(BaseRepository[MessageWorkflowStepError, MessageWorkflowStepErrorCreate]):
    def __init__(self) -> None:
        super().__init__(MessageWorkflowStepError)

    async def record_error(
        self,
        db: AsyncSession,
        *,
        message_workflow_step_id: int,
        error_message: str,
        error_traceback: Optional[str] = None,
    ) -> MessageWorkflowStepError:
        obj = self.model(
            message_workflow_step_id=message_workflow_step_id,
            error_message=error_message,
            error_traceback=error_traceback,
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj


message_workflow_step_error_repository = MessageWorkflowStepErrorRepository()
