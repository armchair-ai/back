import logging
from typing import Dict, Type
from app.core.database import AsyncSessionLocal
from app.repositories.message_workflow_step_repository import message_workflow_step_repository
from app.services.workflow_step_service import workflow_step_service
from app.services.workflow.executors.base import BaseWorkflowExecutor
from app.services.workflow.executors.create_plan_executor import CreatePlanExecutor

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    EXECUTORS: Dict[str, Type[BaseWorkflowExecutor]] = {
        "create_plan": CreatePlanExecutor,
    }

    async def start(self, message_id: int) -> None:
        logger.info(f"WorkflowOrchestrator: Starting workflow for message_id={message_id}")
        await self._advance(message_id=message_id, current_order=0)

    async def advance(self, message_workflow_step_id: int) -> None:
        logger.info(f"WorkflowOrchestrator: Advancing workflow after message_workflow_step_id={message_workflow_step_id}")

        async with AsyncSessionLocal() as db:
            completed_mws = await message_workflow_step_repository.get_with_step(db, id=message_workflow_step_id)
            message_id = completed_mws.message_id
            current_order = completed_mws.workflow_step.order

        await self._advance(message_id=message_id, current_order=current_order)

    async def _advance(self, message_id: int, current_order: int) -> None:
        async with AsyncSessionLocal() as db:
            next_step = await workflow_step_service.get_next_step(db, current_order=current_order)
            if not next_step:
                logger.info(f"Workflow completed for message_id={message_id}. All steps executed.")
                return

        executor_cls = self.EXECUTORS[next_step.name]
        logger.info(f"Advancing message_id={message_id} to step '{next_step.name}' (order={next_step.order})")
        executor = executor_cls()
        await executor.execute(message_id=message_id)


workflow_orchestrator = WorkflowOrchestrator()


