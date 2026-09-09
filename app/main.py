from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt
from jwt.exceptions import (
    ExpiredSignatureError,
    InvalidTokenError,
    DecodeError,
)
from app.api import auth, user, cart, product, order
from app.core.custom_exception import CustomException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.config.secretes import secretes

JWT_SECRET_KEY = secretes.JWT_SECRET_KEY
JWT_ALGORITHM = secretes.JWT_ALGORITHM

app = FastAPI()

PRODUCT_FOLDER = Path("product_image")
# Makes files accessible through:
# http://localhost:8000/uploads/products/filename.jpg
app.mount(
    "/uploads/products",
    StaticFiles(directory=PRODUCT_FOLDER),
    name="product-images",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        '*'
    ],
    allow_credentials=True,
    allow_methods=[
        '*'
    ],
    allow_headers=[
        '*'
    ],
)

@app.middleware("https")
async def validate_auth(request, call_next):
    if request.method == "OPTIONS": 
        return await call_next(request)

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
        encoded_jwt = request.cookies.get("access_token")
        if not encoded_jwt:
            return JSONResponse(
                status_code=401,
                content={
                    'detail': 'Missing or invalid Authorization header'
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


app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(product.router)
app.include_router(order.router)


@app.get("/health")
async def read_root():
    return {
        'Hello': 'World'
    }

@app.exception_handler(CustomException)
async def global_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.message
        }
    )