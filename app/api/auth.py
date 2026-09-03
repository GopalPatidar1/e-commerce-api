from fastapi import APIRouter, Depends, Request
from app.service import auth
from app.config.database import get_db
from app.schema.users import CreateUser, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.rate_limiter import limiter
router = APIRouter(prefix='/auth', tags=[
    'Authentication'
])

@router.post('/login')
@limiter(path='login', max_requests= 5, window_seconds= 60)
async def login(request: Request, login_data: UserLogin, db: AsyncSession= Depends(get_db)):
    return await auth.userLogin(login_data, db)
    
@router.post('/register')
async def registerUser(request: CreateUser, db: AsyncSession = Depends(get_db)):
    return await auth.registerUser(request, db)