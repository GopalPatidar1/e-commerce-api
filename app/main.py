from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    DecodeError,
)
# from app.api import auth, user, category, expense
# from app.core.customException import CustomException
from app.config.secretes import secretes

JWT_SECRET_KEY = secretes.JWT_SECRET_KEY
JWT_ALGORITHM = secretes.JWT_ALGORITHM

app = FastAPI()

@app.middleware("http")
async def validate_auth(request, call_next):
    publicRoutes = [
        '/docs',
        '/openapi.json',
        '/redoc',
        '/health',
        '/auth/login',
        '/auth/register',
        '/logout'
    ]
    if request.url.path not in publicRoutes:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Missing or invalid Authorization header'
                },
            )
        encoded_jwt = auth_header.split(" ", 1)[1]

        if not encoded_jwt:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Missing token'
                },
            )

        try:
            decodeJwt = jwt.decode(encoded_jwt, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])

            user_id = decodeJwt.get("user_id")

            if user_id is None:
                return JSONResponse(
                    status_code=401,
                    content={
                        'detail': 'Invalid token: userId missing'
                    },
                )

            request.state.user_id = int(user_id)
        except ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Token expired'
                },
            )
        except DecodeError:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Malformed token'
                },
            )
        except InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Invalid token'
                },
            )

    response = await call_next(request)
    return response


# app.include_router(auth.router)
# app.include_router(user.router)
# app.include_router(category.router)
# app.include_router(expense.router)

@app.get("/health")
async def read_root():
    return {
        'Hello': 'World'
    }

# @app.exception_handler(CustomException)
# async def global_exception_handler(request: Request, exc: CustomException):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             'error': exc.message
#         }
#     )