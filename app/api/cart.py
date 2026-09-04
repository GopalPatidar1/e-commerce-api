from fastapi import APIRouter, Request, Depends, status
from app.service import cart
from app.config.database import get_db
from app.schema.cart import CartItem, CartResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/cart', tags=[
    'Cart'
])

@router.get('/', response_model=CartResponse)
async def get_cart_list(request: Request, db: AsyncSession = Depends(get_db), limit:int = 10, next_cursor: int | None=None, date_filter:str | None=None):
    user_id =  request.state.user_id
    return await cart.get_cart_list(user_id= user_id, db=db, limit=limit, next_cursor=next_cursor, date_filter= date_filter)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_cart_item(request: Request, data: CartItem, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id
    return await cart.add_cart_item(db, data, user_id)

@router.delete('/{id}')
async def delete_cart_item(id: int,request: Request, db: AsyncSession =Depends(get_db)):
    return await cart.delete_cart_item(id=id, db= db, user_id= request.state.user_id)

