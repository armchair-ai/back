import logging
from pydantic import BaseModel
from app.core.queue import redis_queue

logger = logging.getLogger(__name__)

class EventDispatcher:
    async def dispatch(self, event: BaseModel) -> None:
        try:
            await redis_queue.enqueue(event)
        except Exception as exc:
            logger.error(f"Failed to enqueue event {event}: {exc}")


event_dispatcher = EventDispatcher()
