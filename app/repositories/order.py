from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.order import Order
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def add_order(db:AsyncSession, order):
    db.add(order)

async def get_order_list(db: AsyncSession, user_id: str, next_cursor: int | None, limit:int, start_date,  end_date):
    filter = [Order.user_id == user_id]

    if start_date is not None:
        filter.append(Order.created_at >= start_date)

    if end_date is not None:
        filter.append(Order.created_at <= end_date)

    if next_cursor is not None:
        filter.append(Order.id <= next_cursor)

    result = await db.scalars(
        select(Order)
        .options(selectinload(Order.user), selectinload(Order.product)) 
        .where(*filter)
        .order_by(Order.id.desc())
        .limit(limit+1)
    )

    return result.all()

async def delete_order(id: int, user_id: int, db: AsyncSession):
    return await db.execute(delete(Order).where(
        Order.user_id == user_id,
        Order.id == id
    ))

async def update_order(db: AsyncSession, id:int, user_id: int, data):
     result = await db.execute(
        update(Order)
        .where(
            Order.id == id,
            Order.user_id == user_id
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Order)
       )

     return result.scalar_one_or_none()