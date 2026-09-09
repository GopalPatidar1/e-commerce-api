from redis.asyncio import Redis
from app.config.redis import redis_client
from fastapi.responses import JSONResponse
from fastapi import Request
from functools import wraps

class RateLimiter:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:

        current_count =  self.redis.incr(key)
        if current_count == 1:
            self.redis.expire(
                key,
                window_seconds
            )

        return current_count <= max_requests

limiter_intance = RateLimiter(redis=redis_client)

def limiter(path: str, max_requests: int, window_seconds: int):
    def limiterDecorator(func):
       @wraps(func)
       async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if request is None:
                raise Exception("Request parameter is required")

            client_ip = request.client.host
            key = f"rate_limit:{path}:{client_ip}"
            checkLimit = await limiter_intance.is_allowed(key, max_requests, window_seconds)
            if not checkLimit:
                return JSONResponse(
                status_code=429,
                content={
                    'detail': 'Too many requests'
                },
            )
            return await func(*args, **kwargs)
       return wrapper
    return limiterDecorator


