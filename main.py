from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from city.routers import router as city_router
from temperature.routers import router as temperature_router
from user.routers import router as user_rout, fastapi_users
from user.auth import auth_backend
from user.schemas import UserRead, UserCreate
from redis import asyncio as aioredis


app = FastAPI()


app.include_router(city_router, tags=["City"])
app.include_router(temperature_router, tags=["Temperature"])
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(user_rout, tags=["Route"])


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost",
                              encodings="utf8",
                              decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
