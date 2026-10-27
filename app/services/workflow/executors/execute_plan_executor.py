import logging
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import WorkflowExecutionError
from app.models.message import Message
from app.models.message_workflow_step import MessageWorkflowStep
from app.models.workflow_step import WorkflowStep
from app.repositories.plan_repository import plan_repository
from app.schemas.plan_execution import ExecutePlanResponse
from app.services.agent_service import agent_service
from app.services.artifact_service import artifact_service
from app.services.workflow.executors.base import BaseWorkflowExecutor

logger = logging.getLogger(__name__)


class ExecutePlanExecutor(BaseWorkflowExecutor):
    step_name = "execute_plan"

    async def _execute_step(
        self,
        db: AsyncSession,
        *,
        message: Message,
        step: WorkflowStep,
        mws: MessageWorkflowStep,
    ) -> None:
        plan = await plan_repository.get_by_message_id(db, message_id=message.id)
        prompt = plan.filename

        system_instructions = self._load_system_instructions(
            step.system_instructions
        )

        logger.info(f"Invoking agent for execute_plan, message_id={message.id}")
        agent_result, response_text = await agent_service.chat_structured_with_text(
            prompt=prompt,
            response_structure=ExecutePlanResponse,
            model=step.model,
            system_instructions=system_instructions,
        )
        logger.info(f"Agent finished execute_plan. Structured result: {agent_result}")

        def _get_val(obj: Any, key: str) -> Any:
            return obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)

        success = _get_val(agent_result, "success")
        summary_file = artifact_service.resolve_artifact_path(
            structured_output=agent_result,
            field_keys=("summary_file", "filename"),
            response_text=response_text,
            fallback_pattern="**/summaries/*.md",
        )

        if success is False:
            raise WorkflowExecutionError(
                f"Plan execution reported failure for message_id={message.id}"
            )

        logger.info(f"Plan executed for message_id={message.id}. Success: {success}, Summary file: {summary_file}")
