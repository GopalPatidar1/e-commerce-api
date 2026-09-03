from sqlalchemy import select
from app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

async def createUser(db: AsyncSession, user):
   db.add(user)

async def getUserByEmail(db: AsyncSession , email: str):
     return await db.scalar(
        select(User).where(User.email == email)
    )

async def getUserById(db: AsyncSession, id: int):
     return await db.scalar(
          select(User).where(User.id == id)
     )