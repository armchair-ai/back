from datetime import datetime, timezone
from pydantic import BaseModel, Field


class WorkflowStepCompletedEvent(BaseModel):
    event_name: str = Field(default="WorkflowStepCompleted", frozen=True)
    message_workflow_step_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))