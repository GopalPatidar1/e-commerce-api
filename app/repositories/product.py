from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from app.models.product import Product

async def create_product(db: AsyncSession, data):
   db.add(data)
   return data

async def get_product(db: AsyncSession):
   data = await db.scalars(select(Product))
   return data.all()

async def get_product_by_id(db: AsyncSession, id):
   return await db.scalar(select(Product).where(Product.id == id))

async def update_product(db: AsyncSession, id: int,  data):
   result = await db.execute(
           update(Product)
           .where(Product.id == id,)
           .values(**data.model_dump(exclude_unset=True))
           .returning(Product)
          )
   return result.scalar_one_or_none()

async def delete_product(db: AsyncSession, id: int):
   return await db.execute(delete(Product).where(Product.id == id))