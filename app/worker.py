import asyncio
import logging
import signal
from typing import List, Callable, Awaitable
from pydantic import BaseModel
from app.core.queue import redis_queue
from app.listeners.create_plan_listener import create_plan_listener

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("worker")

WorkerHandler = Callable[[BaseModel], Awaitable[None]]

# Lista de handlers asíncronos que procesa el worker en segundo plano
WORKER_HANDLERS: List[WorkerHandler] = [
    create_plan_listener,
]


class QueueWorker:
    def __init__(self) -> None:
        self._running = True

    def stop(self) -> None:
        logger.info("Stopping worker gracefully...")
        self._running = False

    async def run(self) -> None:
        logger.info("Worker started. Listening for jobs on Redis queue...")
        while self._running:
            try:
                event = await redis_queue.dequeue(timeout=2)
                if event is None:
                    continue

                event_name = getattr(event, "event_name", event.__class__.__name__)
                logger.info(f"Processing event: {event_name}")
                for handler in WORKER_HANDLERS:
                    try:
                        await handler(event)
                    except Exception as handler_err:
                        logger.error(f"Error executing handler {handler.__name__}: {handler_err}", exc_info=True)
            except asyncio.CancelledError:
                break
            except Exception as exc:
                logger.error(f"Worker error: {exc}", exc_info=True)
                await asyncio.sleep(1)


async def main() -> None:
    worker = QueueWorker()
    loop = asyncio.get_running_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, worker.stop)
        except NotImplementedError:
            pass

    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
