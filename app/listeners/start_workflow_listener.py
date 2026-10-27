from pydantic import BaseModel
from app.events.message import MessageCreatedEvent
from app.services.workflow.orchestrator import workflow_orchestrator


async def start_workflow_listener(event: BaseModel) -> None:
    if isinstance(event, MessageCreatedEvent):
        await workflow_orchestrator.start(
            message_id=event.id,
        )
