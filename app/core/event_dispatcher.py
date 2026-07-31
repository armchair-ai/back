from typing import Callable, Awaitable, List
from pydantic import BaseModel

EventHandler = Callable[[BaseModel], Awaitable[None]]

class EventDispatcher:
    def __init__(self) -> None:
        self._handlers: List[EventHandler] = []

    def register(self, handler: EventHandler) -> None:
        self._handlers.append(handler)

    async def dispatch(self, event: BaseModel) -> None:
        for handler in self._handlers:
            await handler(event)

event_dispatcher = EventDispatcher()
