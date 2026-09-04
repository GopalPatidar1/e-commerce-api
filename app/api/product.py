from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.product import CreateProduct, ProductGetResponse
from app.service import product
from app.config.database import get_db
from fastapi import status
from app.auth.authorization import require_permission
from app.auth.permissions import Permission

router = APIRouter(prefix="/product", tags=[
  'Product'
])

@router.get('/', response_model=list[ProductGetResponse])
async def get_product(db: AsyncSession= Depends(get_db)):
  return await product.get_product(db)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(data: CreateProduct, current_user: bool = Depends(require_permission(Permission.PRODUCT_CREATE)), db: AsyncSession = Depends(get_db)):
  return await product.create_product(data=data, db=db)

@router.put('/{id}')
async def update_product(data: CreateProduct, id: int, db: AsyncSession = Depends(get_db), current_user: bool = Depends(require_permission(Permission.PRODUCT_CREATE))):
  return await product.update_product(db= db,data= data, id=id)

@router.delete('/{id}')
async def delete_product(id: int, db: AsyncSession= Depends(get_db), current_user: bool = Depends(require_permission(Permission.PRODUCT_CREATE))):
  return await product.delete_product(db=db, id=id)
  
