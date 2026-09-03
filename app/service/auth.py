from app.models.users import User
from app.repository import user as userRepo
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone
from app.config.secretes import secretes
from app.core.customException import CustomException
import jwt

async def registerUser(request, db):
    try:
      user = User(
          firstname=request.firstname,
          lastname=request.lastname,
          email=request.email,
          password=request.password
      )
      await userRepo.createUser(db, user)

      await db.commit()
      await db.refresh(user)
      
      return {
          "id": user.id,
          "firstname": user.firstname,
          "email": user.email
      }

    except Exception as e:
        await db.rollback()
        raise CustomException(status.HTTP_422_UNPROCESSABLE_CONTENT, 'Something went wrong')

def createAccessToken(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=secretes.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = { "user_id": str(user_id), "exp": expire }

    return jwt.encode(
        payload,
        secretes.JWT_SECRET_KEY,
        algorithm=secretes.JWT_ALGORITHM
    )

async def userLogin(request, db) -> str:
   user = await userRepo.getUserByEmail(db, request.email)

   if user is None:
        raise CustomException(status.HTTP_401_UNAUTHORIZED, 'Incorrect email or password')

   check = user.verify_password_hash(request.password)

   if not check:
        raise CustomException(status.HTTP_401_UNAUTHORIZED, 'Incorrect email or password')

   return createAccessToken(user.id)