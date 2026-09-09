from app.repositories import product 
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.custom_exception import CustomException
from fastapi import status, UploadFile
from app.models.product import Product
from app.schema.product import CreateProduct
from pathlib import Path
from uuid import uuid4


PRODUCT_IMAGE_DIR = Path("product_image")

PRODUCT_IMAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

async def save_product_image(image: UploadFile) -> str:
    extension = Path(image.filename or "").suffix.lower()

    filename = f"{uuid4().hex}{extension}"

    file_path = PRODUCT_IMAGE_DIR / filename

    with file_path.open("wb") as file:
        while chunk := await image.read(1024 * 1024):
            file.write(chunk)

    return f"/uploads/products/{filename}"

async def create_product(image: UploadFile, data: CreateProduct, db: AsyncSession, user_id: str):
    try:

     img_path = await save_product_image(image)
     
     product_data = Product(
       name=data.name,
       description=data.description,
       amount=data.amount,
       img_path=img_path,
       user_id=user_id
     )
     

     await product.create_product(db=db, data=product_data)

     await db.commit()

     await db.refresh(product_data)
 
     return { "id": product_data.id }

    except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR)

async def get_product(db: AsyncSession):
  try:
   return await product.get_product(db)
  except Exception as e:
    await db.rollback()
    raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to fetch products")

async def update_product(db: AsyncSession, id: int, data):
   try:
     product_data =  await product.update_product(db=db, data=data, id=id)
     if product_data is None:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Product not found")
     await db.commit()

     return product_data
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to update product")

async def delete_product(db: AsyncSession, id: int):
   try:
     result =  await product.delete_product(db= db, id= id)

     if result.rowcount == 0:
        raise CustomException(status.HTTP_404_NOT_FOUND, "Product not found")

     await db.commit()

     return {
       'message': 'Product deleted successfully'
     }
   except CustomException:
     raise
   except Exception as e:
     await db.rollback()
     raise CustomException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete product")