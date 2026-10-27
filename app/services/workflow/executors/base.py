import logging
import traceback
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.core.event_dispatcher import event_dispatcher
from app.events.workflow import WorkflowStepCompletedEvent
from app.models.message import Message
from app.models.message_workflow_step import MessageWorkflowStep
from app.models.workflow_step import WorkflowStep
from app.repositories.message_repository import message_repository
from app.repositories.message_workflow_step_repository import message_workflow_step_repository
from app.repositories.message_workflow_step_error_repository import message_workflow_step_error_repository
from app.services.workflow_step_service import workflow_step_service

logger = logging.getLogger(__name__)


class BaseWorkflowExecutor(ABC):
    step_name: str

    def _load_system_instructions(self, filename: str) -> Optional[str]:
        if not filename:
            return None
        path = Path("app/workflows/instructions") / Path(filename).name
        return path.read_text(encoding="utf-8") if path.is_file() else None

    async def execute(self, message_id: int) -> None:
        started_at = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as db:
            message = await message_repository.get(db, id=message_id)
            step = await workflow_step_service.get_by_name(db, name=self.step_name)

            mws = await message_workflow_step_repository.create_step(
                db,
                message_id=message.id,
                workflow_step_id=step.id,
                status="running",
                started_at=started_at,
            )
            logger.info(f"Recorded start of message_workflow_step id={mws.id} for step '{self.step_name}' (message_id={message.id})")

            try:
                await self._execute_step(db, message=message, step=step, mws=mws)

                finished_at = datetime.now(timezone.utc)
                await message_workflow_step_repository.mark_finished(
                    db,
                    id=mws.id,
                    status="completed",
                    finished_at=finished_at,
                )
                logger.info(f"Marked message_workflow_step id={mws.id} as completed for step '{self.step_name}'")

                # Disparar evento para que el orquestador avance al siguiente paso
                completed_event = WorkflowStepCompletedEvent(
                    message_workflow_step_id=mws.id,
                )
                await event_dispatcher.dispatch(completed_event)
                logger.info(f"Dispatched WorkflowStepCompletedEvent for step '{self.step_name}' with message_workflow_step_id={mws.id}")

            except Exception as exc:
                tb = traceback.format_exc()
                logger.error(f"Error executing step '{self.step_name}' for message_id={message_id}: {exc}", exc_info=True)
                await message_workflow_step_repository.mark_failed(db, id=mws.id)
                await message_workflow_step_error_repository.record_error(
                    db,
                    message_workflow_step_id=mws.id,
                    error_message=str(exc),
                    error_traceback=tb,
                )
                raise

    @abstractmethod
    async def _execute_step(
        self,
        db: AsyncSession,
        *,
        message: Message,
        step: WorkflowStep,
        mws: MessageWorkflowStep,
    ) -> None:
        """Lógica específica del paso que debe implementar cada ejecutor concreto."""
        pass
