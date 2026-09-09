from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.cart import Cart
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def add_cart(db:AsyncSession, cart):
    db.add(cart)

async def get_cart_list(db: AsyncSession, user_id: str, next_cursor: int | None, limit:int, start_date,  end_date):
    filter = [Cart.user_id == user_id]

    if start_date is not None:
        filter.append(Cart.created_at >= start_date)

    if end_date is not None:
        filter.append(Cart.created_at <= end_date)

    if next_cursor is not None:
        filter.append(Cart.id <= next_cursor)

    result = await db.scalars(
        select(Cart)
        .options(selectinload(Cart.user), selectinload(Cart.product)) 
        .where(*filter)
        .order_by(Cart.id.desc())
        .limit(limit+1)
    )

    return result.all()

async def delete_cart(id: int, user_id: int, db: AsyncSession):
    return await db.execute(delete(Cart).where(
        Cart.user_id == user_id,
        Cart.id == id
    ))

async def update_cart(db: AsyncSession, id:int, user_id: int, data):
     result = await db.execute(
        update(Cart)
        .where(
            Cart.id == id,
            Cart.user_id == user_id
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Cart)
       )

     return result.scalar_one_or_none()