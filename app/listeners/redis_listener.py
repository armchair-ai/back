import logging
from pydantic import BaseModel
from app.core.redis import redis_client
from app.core.event_dispatcher import event_dispatcher

logger = logging.getLogger(__name__)

async def redis_event_publisher(event: BaseModel) -> None:
    if hasattr(event, "event_name"):
        event_name: str = getattr(event, "event_name")
        try:
            await redis_client.publish(event_name, event.model_dump_json())
        except Exception as exc:
            logger.error(f"Failed to publish event '{event_name}' to Redis: {exc}")

event_dispatcher.register(redis_event_publisher)
