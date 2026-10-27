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
from app.services.workflow_step_service import workflow_step_service
from app.schemas.plan import PlanCreate, PlanCreateResponse
from app.services.agent_service import agent_service
from app.services.workflow.executors.base import BaseWorkflowExecutor

logger = logging.getLogger(__name__)

# Mapa de schemas conocidos según el nombre en base de datos
SCHEMA_MAP: dict[str, Type[BaseModel]] = {
    "PlanCreateResponse": PlanCreateResponse,
    "PlannerResponse": PlanCreateResponse,
}


class CreatePlanExecutor(BaseWorkflowExecutor):
    async def execute(self, message_id: int) -> None:
        started_at = datetime.now(timezone.utc)

        async with AsyncSessionLocal() as db:
            message = await message_repository.get(db, id=message_id)
            step = await workflow_step_service.get_by_name(db, name="create_plan")

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
            response_schema = SCHEMA_MAP.get(step.response_schema or "", PlanCreateResponse)

            logger.info(f"Invoking agent for create_plan, message_id={message_id}")
            agent_result: Any = await agent_service.chat_structured(
                prompt=message.text,
                response_structure=response_schema,
                model=step.model,
                system_instructions=system_instructions,
            )

            # Extraer campos de resultado de forma segura (objeto o dict)
            def _get_val(obj: Any, key: str) -> Any:
                return obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)

            success = _get_val(agent_result, "success")
            filename = _get_val(agent_result, "filename")

            # Ejecutar guardado del plan si el resultado fue exitoso
            if agent_result and success and filename:
                plan_in = PlanCreate(
                    filename=str(filename).strip(),
                    message_id=message.id,
                )
                await plan_repository.create(db, obj_in=plan_in)
                logger.info(f"Plan created successfully with filename: {plan_in.filename}")

            finished_at = datetime.now(timezone.utc)

            # Registrar finalización en message_workflow_step
            await message_workflow_step_repository.mark_finished(
                db,
                id=mws.id,
                finished_at=finished_at,
            )
            logger.info(f"Marked message_workflow_step id={mws.id} as finished")

            # Lanzar evento WorkflowStepCompletedEvent con message_workflow_step_id
            completed_event = WorkflowStepCompletedEvent(
                message_workflow_step_id=mws.id,
            )
            await event_dispatcher.dispatch(completed_event)
            logger.info(f"Dispatched WorkflowStepCompletedEvent for step '{step.name}' with message_workflow_step_id={mws.id}")

