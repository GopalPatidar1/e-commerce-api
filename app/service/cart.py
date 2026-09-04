from app.repositories import cart
from app.models.cart import Cart
from fastapi.responses import JSONResponse
from app.core.custom_exception import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.schema.cart import CartDateFilter
from datetime import datetime, timedelta

async def add_cart_item(db: AsyncSession, cart_data, user_id: int):
    try:
      cartData = Cart(
          product_id=cart_data.product_id,
          quantity=cart_data.quantity,
          user_id= user_id,
      )
      
      await cart.add_cart(db, cartData)

      await db.commit()
      await db.refresh(cartData)

      return { "id": cartData.id }
    except Exception as e:
        await db.rollback()
        raise CustomException(500, "Something went wrong") 

async def get_cart_list(user_id: int, db: AsyncSession, limit: int, next_cursor: int|None, date_filter: CartDateFilter | None):
   now = datetime.now()
   start_date, end_date = None, None
   if date_filter == CartDateFilter.PAST_WEEK:
       start_date = now - timedelta(days=7)
       end_date = now
   
   elif date_filter == CartDateFilter.PAST_MONTH:
       start_date = now - timedelta(days=30)
       end_date = now
   
   elif date_filter == CartDateFilter.LAST_3_MONTHS:
       start_date = now - timedelta(days=90)
       end_date = now
   
   result =  await cart.get_cart_list(db= db, user_id= user_id, limit= limit, next_cursor=next_cursor,  start_date=start_date,end_date= end_date,)
   next_cursor = result[-1].id if result else None
   avail_next = len(result) > limit
   return {"next_cursor": next_cursor, "avail_next":avail_next ,"result": result[:limit]}

async def delete_cart_item(db: AsyncSession, user_id: int, id: int):
   result = await cart.delete_cart(db=db, user_id=user_id, id=id)

   if result.rowcount == 0:
      raise CustomException(404,"Cart not found") 
   
   return {
       'success': True
   }
