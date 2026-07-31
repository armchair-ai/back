from datetime import datetime, timezone
from pydantic import BaseModel, Field

class OrderCreatedEvent(BaseModel):
    event_name: str = Field(default="OrderCreated", frozen=True)
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
