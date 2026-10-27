from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageWorkflowStepErrorBase(BaseModel):
    error_message: str
    error_traceback: Optional[str] = None


class MessageWorkflowStepErrorCreate(MessageWorkflowStepErrorBase):
    message_workflow_step_id: int


class MessageWorkflowStepErrorResponse(MessageWorkflowStepErrorBase):
    id: int
    message_workflow_step_id: int
    created_at: datetime

    class Config:
        from_attributes = True
