from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional

class MessageBase(BaseModel):
    text: str = Field(..., min_length=1)

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    order_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
