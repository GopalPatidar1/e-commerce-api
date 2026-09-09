from fastapi import APIRouter, Depends, Request, Response
from app.service import auth
from app.config.database import get_db
from app.schema.users import CreateUser, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.rate_limiter import limiter
from app.config.secretes import secretes

router = APIRouter(prefix='/auth', tags=[
    'Authentication'
])

@router.post('/login')
@limiter(path='login', max_requests= 5, window_seconds= 60)
async def login(request: Request, response:Response, login_data: UserLogin, db: AsyncSession= Depends(get_db)):
    access_token = await auth.userLogin(login_data, db)
    response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,       # localhost HTTP
            samesite= "lax", # localhost HTTP
            max_age= 60 * secretes.ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    return {
        'message': 'Login successful'
    }
    
@router.post('/register')
async def registerUser(request: CreateUser, db: AsyncSession = Depends(get_db)):
    return await auth.registerUser(request, db)