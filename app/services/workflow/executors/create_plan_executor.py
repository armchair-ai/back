import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ArtifactNotFoundError
from app.models.message import Message
from app.models.message_workflow_step import MessageWorkflowStep
from app.models.workflow_step import WorkflowStep
from app.repositories.plan_repository import plan_repository
from app.schemas.plan import PlanCreate, PlanCreateResponse
from app.services.agent_service import agent_service
from app.services.artifact_service import artifact_service
from app.services.workflow.executors.base import BaseWorkflowExecutor

logger = logging.getLogger(__name__)


class CreatePlanExecutor(BaseWorkflowExecutor):
    step_name = "create_plan"

    async def _execute_step(
        self,
        db: AsyncSession,
        *,
        message: Message,
        step: WorkflowStep,
        mws: MessageWorkflowStep,
    ) -> None:
        system_instructions = self._load_system_instructions(
            step.system_instructions
        )

        logger.info(f"Invoking agent for create_plan, message_id={message.id}")
        agent_result, response_text = await agent_service.chat_structured_with_text(
            prompt=message.text,
            response_structure=PlanCreateResponse,
            model=step.model,
            system_instructions=system_instructions,
        )
        logger.info(f"Agent finished create_plan. Structured result: {agent_result}")

        plan_path = artifact_service.resolve_artifact_path(
            structured_output=agent_result,
            field_keys=("filename", "plan_file"),
            response_text=response_text,
            fallback_pattern="**/*.md",
        )

        if not plan_path:
            raise ArtifactNotFoundError(
                f"Could not determine or locate the plan file for message_id={message.id}"
            )

        plan_in = PlanCreate(
            filename=plan_path,
            message_id=message.id,
        )
        await plan_repository.create(db, obj_in=plan_in)
        logger.info(f"Plan saved to database with filename: {plan_in.filename}")
