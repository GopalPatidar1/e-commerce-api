from sqlalchemy import select, delete, update
from sqlalchemy.orm import selectinload
from app.models.transactions import Transaction
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def add_transaction(db:AsyncSession, order):
    db.add(order)

async def update_transaction(db: AsyncSession, id:int, user_id: int, data):
     result = await db.execute(
        update(Transaction)
        .where(
            Transaction.id == id,
            Transaction.user_id == user_id
        )
        .values(**data.model_dump(exclude_unset=True))
        .returning(Transaction)
       )

     return result.scalar_one_or_none()