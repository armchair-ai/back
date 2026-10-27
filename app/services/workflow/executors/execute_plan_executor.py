import logging
from datetime import datetime, timezone
from typing import Any, Type
from pydantic import BaseModel

from app.core.database import AsyncSessionLocal
from app.core.event_dispatcher import event_dispatcher
from app.events.workflow import WorkflowStepCompletedEvent
from app.repositories.message_repository import message_repository
from app.repositories.message_workflow_step_repository import message_workflow_step_repository
from app.repositories.plan_repository import plan_repository
from app.schemas.plan_execution import ExecutePlanResponse
from app.services.agent_service import agent_service
from app.services.workflow.executors.base import BaseWorkflowExecutor
from app.services.workflow_step_service import workflow_step_service

logger = logging.getLogger(__name__)

SCHEMA_MAP: dict[str, Type[BaseModel]] = {
    "ExecutePlanResponse": ExecutePlanResponse,
}


class ExecutePlanExecutor(BaseWorkflowExecutor):
    async def execute(self, message_id: int) -> None:
        started_at = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as db:
            message = await message_repository.get(db, id=message_id)
            step = await workflow_step_service.get_by_name(db, name="execute_plan")
            plan = await plan_repository.get_by_message_id(db, message_id=message_id)

            mws = await message_workflow_step_repository.create_step(
                db,
                message_id=message.id,
                workflow_step_id=step.id,
                started_at=started_at,
            )
            logger.info(f"Recorded start of message_workflow_step id={mws.id} for message_id={message.id}, step_id={step.id}")

            system_instructions = self._load_system_instructions(
                step.system_instructions
            )
            response_schema = SCHEMA_MAP.get(step.response_schema or "", ExecutePlanResponse)

            prompt = plan.filename if (plan and plan.filename) else "Execute the implementation plan."

            logger.info(f"Invoking agent for execute_plan, message_id={message_id}")
            agent_result, response_text = await agent_service.chat_structured_with_text(
                prompt=prompt,
                response_structure=response_schema,
                model=step.model,
                system_instructions=system_instructions,
            )
            logger.info(f"Agent finished execute_plan. Structured result: {agent_result}")

            def _get_val(obj: Any, key: str) -> Any:
                return obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)

            success = _get_val(agent_result, "success")
            summary_file = _get_val(agent_result, "summary_file") or _get_val(agent_result, "filename")

            # Si no vino en el structured output, intentar extraer enlace file:// o ruta del texto
            if not summary_file and response_text:
                import re
                match = re.search(r"file://([^\s\)\"']+\.md)", response_text) or re.search(r"(/tmp/[^\s\)\"']+\.md)", response_text)
                if match:
                    summary_file = match.group(1)

            logger.info(f"Plan executed for message_id={message_id}. Success: {success}, Summary file: {summary_file}")

            finished_at = datetime.now(timezone.utc)

            await message_workflow_step_repository.mark_finished(
                db,
                id=mws.id,
                finished_at=finished_at,
            )
            logger.info(f"Marked message_workflow_step id={mws.id} as finished")

            completed_event = WorkflowStepCompletedEvent(
                message_workflow_step_id=mws.id,
            )
            await event_dispatcher.dispatch(completed_event)
            logger.info(f"Dispatched WorkflowStepCompletedEvent for step '{step.name}' with message_workflow_step_id={mws.id}")
