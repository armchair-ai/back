import json
import logging
import uuid
from typing import Any, Dict, Optional, Type
from pydantic import BaseModel
from app.core.redis import redis_client
from app.events.message import MessageCreatedEvent

logger = logging.getLogger(__name__)

EVENT_TYPES: Dict[str, Type[BaseModel]] = {
    "MessageCreated": MessageCreatedEvent,
}


class RedisQueue:
    def __init__(self, key_prefix: str = "queue:") -> None:
        self.key_prefix = key_prefix

    async def enqueue(self, event: BaseModel, queue_name: str = "default") -> str:
        job_id = str(uuid.uuid4())
        event_name = getattr(event, "event_name", event.__class__.__name__)
        job_data = {
            "id": job_id,
            "event_name": event_name,
            "payload": event.model_dump(mode="json"),
        }
        queue_key = f"{self.key_prefix}{queue_name}"
        await redis_client.rpush(queue_key, json.dumps(job_data))
        logger.info(f"Job enqueued: {job_id} ({event_name}) in {queue_key}")
        return job_id

    async def dequeue(self, queue_name: str = "default", timeout: int = 2) -> Optional[BaseModel]:
        queue_key = f"{self.key_prefix}{queue_name}"
        try:
            result = await redis_client.blpop(queue_key, timeout=timeout)
        except (TimeoutError, Exception) as exc:
            if "Timeout" in str(type(exc).__name__) or "Timeout" in str(exc):
                return None
            logger.error(f"Error reading from Redis queue: {exc}")
            return None

        if not result:
            return None

        _, raw_data = result
        try:
            job = json.loads(raw_data)
            event_name = job.get("event_name", "")
            payload = job.get("payload", {})
            event_cls = EVENT_TYPES.get(event_name)
            if event_cls:
                return event_cls.model_validate(payload)
            logger.warning(f"Unknown event type: {event_name}")
        except Exception as exc:
            logger.error(f"Failed to decode job from queue: {exc}")
        return None


redis_queue = RedisQueue()
