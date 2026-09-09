from app.repositories import order
from app.models.order import Order
from fastapi.responses import JSONResponse
from app.core.custom_exception import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.schema.order import OrderDateFilter, OrderDateFilter
from datetime import datetime, timedelta
from app.repositories.product import get_product_by_id

async def add_order_item(db: AsyncSession, order_data, user_id: int):
    try:
      getAmount = await get_product_by_id(db, order_data.product_id)
      
      orderData = Order(
          product_id=order_data.product_id,
          quantity=order_data.quantity,
          user_id= user_id,
          amount=getAmount.amount
      )
      
      await order.add_order(db, orderData)

      await db.commit()
      await db.refresh(orderData)

      return {
          "id": orderData.id,
          "amount": orderData.amount,
          "description": orderData.quantity,
      }
    except Exception as e:
        await db.rollback()
        raise CustomException(500, "Something went wrong") 

async def get_order_list(user_id: int, db: AsyncSession, limit: int, next_cursor: int|None, date_filter: OrderDateFilter | None):
   now = datetime.now()
   start_date, end_date = None, None
   if date_filter == OrderDateFilter.PAST_WEEK:
       start_date = now - timedelta(days=7)
       end_date = now
   
   elif date_filter == OrderDateFilter.PAST_MONTH:
       start_date = now - timedelta(days=30)
       end_date = now
   
   elif date_filter == OrderDateFilter.LAST_3_MONTHS:
       start_date = now - timedelta(days=90)
       end_date = now
   
   result =  await order.get_order_list(db= db, user_id= user_id, limit= limit, next_cursor=next_cursor,  start_date=start_date,end_date= end_date,)
   next_cursor = result[-1].id if result else None
   avail_next = len(result) > limit
   return {"next_cursor": next_cursor, "avail_next":avail_next ,"result": result[:limit]}

async def delete_order_item(db: AsyncSession, user_id: int, id: int):
   result = await order.delete_order(db=db, user_id=user_id, id=id)

   if result.rowcount == 0:
      raise CustomException(404,"Order not found") 

   await db.commit()
   
   return {
       'success': True
   }

async def update_order_item(db: AsyncSession, id: int, user_id: int, data,):
   result = await order.update_order(db= db, id= id, user_id= user_id, data= data)

   if result is None:
      raise CustomException(404,"Order not found") 

   await db.commit()
   
   return result