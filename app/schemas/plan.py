from pydantic import BaseModel, Field


class PlanBase(BaseModel):
    filename: str = Field(..., min_length=1)


class PlanCreate(PlanBase):
    message_id: int


class PlanCreateResponse(BaseModel):
    success: bool = Field(default=False)
    filename: str = Field(default="")
