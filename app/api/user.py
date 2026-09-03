from fastapi import APIRouter, Depends, Request
from app.service import user
from app.config.database import get_db
from app.schema.users import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/user', tags=[
    'User'
])

@router.get('/profile', response_model= UserResponse)
async def getUserProfile(request:Request, db: AsyncSession = Depends(get_db)):
    info = await user.getUserProfileById(db, request.state.userId)
    return info
    

