from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
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
from app.config.database import get_db
from app.service.razorpay import process_payment
import json
import hmac
import hashlib

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
        '/razorpay/webhook',
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

@app.post('/razorpay/webhook')
async def webHook(request: Request, db: AsyncSession = Depends(get_db)):
    body = await request.body()

    # 2. Get Razorpay signature
    received_signature = request.headers.get("X-Razorpay-Signature")

    if not received_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing Razorpay signature"
        )

    # 3. Your Razorpay webhook secret
    webhook_secret = secretes.RAZORPAY_WEBHOOK_SECRET

    # 4. Generate signature
    expected_signature = hmac.new(
        webhook_secret.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    # 5. Compare signatures
    if not hmac.compare_digest(
        expected_signature,
        received_signature
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Razorpay webhook signature"
        )

    data = json.loads(body)
    event = data.get("event")
    if event == "payment_link.paid":
        payment_link = (
            data
            .get("payload", {})
            .get("payment_link", {})
            .get("entity", {})
        )

        payment = (
            data
            .get("payload", {})
            .get("payment", {})
            .get("entity", {})
        )

        reference_id = payment_link.get("reference_id")
        payment_link_id = payment_link.get("id")
        payment_id = payment.get("id")
        payment_status = payment.get("status")

        if not reference_id:
            raise HTTPException(
                status_code=400,
                detail="Missing reference_id"
            )

        order_id = reference_id.split("_")[-1]

        await process_payment(
            order_id=int(order_id),
            payment_link_id=payment_link_id,
            payment_id=payment_id,
            db=db
        )
        
@app.get("/health")
async def read_root():
    return {
        'Hello': 'World'
    }

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(product.router)
app.include_router(order.router)

@app.exception_handler(CustomException)
async def global_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'error': exc.message
        }
    )