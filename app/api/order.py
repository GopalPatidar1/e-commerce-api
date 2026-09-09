from fastapi import APIRouter, Request, Depends, status
from app.service import order
from app.config.database import get_db
from app.schema.order import OrderItem, OrderResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/orders', tags=[
    'Order'
])

@router.get('/', response_model=OrderResponse)
async def get_order_list(request: Request, db: AsyncSession = Depends(get_db), limit:int = 10, next_cursor: int | None=None, date_filter:str | None=None):
    user_id =  request.state.user_id
    return await order.get_order_list(user_id= user_id, db=db, limit=limit, next_cursor=next_cursor, date_filter= date_filter)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_expense_item(request: Request, data: OrderItem, db: AsyncSession = Depends(get_db)):
    user_id = request.state.user_id
    return await order.add_order_item(db, data, user_id)

@router.put('/{id}')
async def update_expense_item(id: int, request: Request, item: OrderItem, db: AsyncSession = Depends(get_db)):
    return await order.update_order_item(user_id=request.state.user_id, data=item, db=db, id=id)

@router.delete('/{id}')
async def delete_expense_item(id: int,request: Request, db: AsyncSession =Depends(get_db)):
    return await order.delete_order_item(id=id, db= db, user_id= request.state.user_id)

@router.get('/{id}')
def get_expense_item(id: int):
    return {
        'id': id,
        'title': f'Expense item {id}',
        'completed': False
    }
