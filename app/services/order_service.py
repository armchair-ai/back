from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ModelNotFoundError
from app.repositories.order_repository import order_repository
from app.schemas.order import OrderCreate
from app.models.order import Order

class OrderService:
    async def create_order(self, db: AsyncSession, order_in: OrderCreate) -> Order:
        return await order_repository.create(db, obj_in=order_in)

    async def get_order(self, db: AsyncSession, order_id: int) -> Order:
        order = await order_repository.get_with_messages(db, id=order_id)
        if not order:
            raise ModelNotFoundError("Order not found")
        return order

order_service = OrderService()
