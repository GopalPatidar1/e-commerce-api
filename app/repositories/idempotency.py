from sqlalchemy import select
from app.models.idempotency_keys import IdempotencyKey
from sqlalchemy.ext.asyncio import AsyncSession

async def add_idempotency(db:AsyncSession, data):
    db.add(data)

async def get_idempotency_by_id(db: AsyncSession, id: int, user_id: int):
     return await db.scalar(
          select(IdempotencyKey).where(IdempotencyKey.idempotency_key == id, IdempotencyKey.user_id==user_id)
     )
