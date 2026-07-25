from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List
from app.schemas.message import MessageResponse

class OrderBase(BaseModel):
    description: str = Field(..., min_length=1)

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []

    model_config = ConfigDict(from_attributes=True)
