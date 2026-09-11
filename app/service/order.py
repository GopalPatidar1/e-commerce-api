from app.repositories import order, idempotency
from app.models.order import Order
from app.models.idempotency_keys import IdempotencyKey
from app.models.transactions import Transaction
from fastapi.responses import JSONResponse
from app.core.custom_exception import CustomException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.schema.order import OrderDateFilter, OrderDateFilter
from datetime import datetime, timedelta
from app.repositories.product import get_product_by_id
from app.config.razorpay import razorpay
from app.repositories.user import getUserById
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

async def add_idempotency_record(idempotency_record, user_id, idempotency_key, db: AsyncSession):
   
    await idempotency.add_idempotency(db, idempotency_record)
    try:
        await db.flush()
        return True, None
    except IntegrityError:
        await db.rollback()

        result = await idempotency.get_idempotency_by_id(db, idempotency_key, user_id)

        if result is not None:
            if result.response_body is not None:
                    return False, result.response_body
    
            if result.idempotency_key != idempotency_key:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        "Idempotency-Key was already used "
                        "with a different request."
                    ),
                )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Request is already being processed.",
        )

async def add_order_item(db: AsyncSession, order_data, user_id: int):

    idempotency_key = order_data.idempotency_key
    try:
      idempotency_record = IdempotencyKey(user_id=user_id, idempotency_key=idempotency_key, )
      cont, data  = await add_idempotency_record(idempotency_record, user_id, idempotency_key, db)
      
      if cont is False:
         return data

      getAmount = await get_product_by_id(db, order_data.product_id)
      
      orderData = Order(
          product_id=order_data.product_id,
          quantity=order_data.quantity,
          user_id= user_id,
          amount=getAmount.amount
      )

      
      await order.add_order(db, orderData)

      await db.flush()

      total_amount = getAmount.amount * order_data.quantity

      payment_link = razorpay.generate_payment_link(
            amount=total_amount,
            description=f"Payment for Order #{orderData.id}",
            reference_id=f"ORDER_{orderData.id}",
            user_id=user_id,
        )

      transaction = Transaction(
            user_id=user_id,
            order_id=orderData.id,
            payment_link_id=payment_link["id"],
            amount=total_amount,
            currency="INR",
            status="pending",
          
        )

      db.add(transaction)

      response_body =  {
          "id": orderData.id,
          "amount": orderData.amount,
          "description": orderData.quantity,
          "payment_url": payment_link["short_url"],
          "payment_link_id": payment_link["id"]
      }
  
      idempotency_record.response_status = 201
      idempotency_record.response_body = response_body
      idempotency_record.resource_id = str(orderData.id)

      await db.commit()
 
      return response_body
    except Exception as e:
        await db.rollback()
        raise CustomException(500, str(e)) 

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