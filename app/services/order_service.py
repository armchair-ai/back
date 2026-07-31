from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ModelNotFoundError
from app.core.redis import redis_client
from app.events.order import OrderCreatedEvent
from app.repositories.order_repository import order_repository
from app.schemas.order import OrderCreate
from app.models.order import Order

class OrderService:
    async def create_order(self, db: AsyncSession, order_in: OrderCreate) -> Order:
        order = await order_repository.create(db, obj_in=order_in)
        event = OrderCreatedEvent(id=order.id)
        await redis_client.publish(event.event_name, event.model_dump_json())
        return order



    async def get_order(self, db: AsyncSession, order_id: int) -> Order:
        order = await order_repository.get_with_messages(db, id=order_id)
        if not order:
            raise ModelNotFoundError("Order not found")
        return order

    async def get_all_orders(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Order]:
        return await order_repository.get_all_with_messages(db, skip=skip, limit=limit)

order_service = OrderService()
