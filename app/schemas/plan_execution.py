from pydantic import BaseModel, Field


class ExecutePlanResponse(BaseModel):
    success: bool = Field(default=False)
    summary_file: str = Field(default="")
