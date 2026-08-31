from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class PlanBase(BaseModel):
    filename: str = Field(..., min_length=1)


class PlanCreate(PlanBase):
    message_id: int


class PlanResponse(PlanBase):
    id: int
    message_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
