from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageWorkflowStepResponse(BaseModel):
    id: int
    message_id: int
    workflow_step_id: int
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
