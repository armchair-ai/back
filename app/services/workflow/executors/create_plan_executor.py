import logging
from datetime import datetime, timezone
from pathlib import Path
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
            agent_result, response_text = await agent_service.chat_structured_with_text(
                prompt=message.text,
                response_structure=response_schema,
                model=step.model,
                system_instructions=system_instructions,
            )
            logger.info(f"Agent finished create_plan. Structured result: {agent_result}")

            # Extraer campos de resultado de forma segura
            def _get_val(obj: Any, key: str) -> Any:
                return obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None)

            plan_path: str | None = None

            # 1. Intentar desde structured output
            fn = _get_val(agent_result, "filename")
            if fn and str(fn).strip():
                clean_fn = str(fn).strip()
                if Path(clean_fn).exists():
                    plan_path = clean_fn

            # 2. Intentar extraer del texto de la respuesta (enlaces file:// o rutas /tmp/...)
            if not plan_path and response_text:
                import re
                match = re.search(r"file://([^\s\)\"']+\.md)", response_text) or re.search(r"(/tmp/[^\s\)\"']+\.md)", response_text)
                if match:
                    candidate = match.group(1)
                    if Path(candidate).exists():
                        plan_path = candidate

            # 3. Fallback: buscar el archivo .md más reciente en el brain de Antigravity
            if not plan_path:
                brain_dir = Path("/tmp/.gemini/antigravity/brain")
                if brain_dir.exists():
                    md_files = list(brain_dir.glob("**/*.md"))
                    if md_files:
                        latest_file = max(md_files, key=lambda f: f.stat().st_mtime)
                        plan_path = str(latest_file)

            # Guardar el plan en la base de datos si se obtuvo una ruta válida
            if plan_path:
                plan_in = PlanCreate(
                    filename=plan_path,
                    message_id=message.id,
                )
                await plan_repository.create(db, obj_in=plan_in)
                logger.info(f"Plan saved to database with filename: {plan_in.filename}")
            else:
                logger.warning(f"Could not determine plan file path for message_id={message_id}")

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

