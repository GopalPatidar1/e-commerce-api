from app.repositories.order import update_order, getOrderById
from app.repositories.transactions import update_transaction
from app.config.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.order import UpdateOrderItemNoneRequiredField


async def process_payment(order_id: int, payment_link_id: str, payment_id: str, db: AsyncSession):
    # await update_order(db=db, status)
    order = await getOrderById(db, order_id)
    await update_order(db=db, id=order_id, user_id=order.user_id,  data=UpdateOrderItemNoneRequiredField(
        status= 'processing'
    ))
    # pass
    await db.commit()
    return

