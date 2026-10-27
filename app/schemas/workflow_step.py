from typing import Optional
from pydantic import BaseModel, Field


class WorkflowStepBase(BaseModel):
    name: str = Field(..., min_length=1)
    order: int = Field(..., gt=0)
    model: str = Field(..., min_length=1)
    system_instructions: str = Field(..., min_length=1)
    response_schema: Optional[str] = None
    skills_paths: Optional[str] = None


class WorkflowStepCreate(WorkflowStepBase):
    pass


class WorkflowStepResponse(WorkflowStepBase):
    id: int

    class Config:
        from_attributes = True
