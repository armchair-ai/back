from pydantic import BaseModel
from app.events.workflow import WorkflowStepCompletedEvent
from app.services.workflow.orchestrator import workflow_orchestrator


async def advance_workflow_listener(event: BaseModel) -> None:
    if isinstance(event, WorkflowStepCompletedEvent):
        await workflow_orchestrator.advance(
            message_workflow_step_id=event.message_workflow_step_id,
        )
