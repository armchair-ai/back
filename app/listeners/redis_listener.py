from pydantic import BaseModel
from app.core.redis import redis_client
from app.core.event_dispatcher import event_dispatcher

async def redis_event_publisher(event: BaseModel) -> None:
    if hasattr(event, "event_name"):
        event_name: str = getattr(event, "event_name")
        await redis_client.publish(event_name, event.model_dump_json())

event_dispatcher.register(redis_event_publisher)
