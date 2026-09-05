from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.db.database import Base, engine
from app.db import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(
    title="City Temperature Management API",
    lifespan=lifespan,
)

app.include_router(api_router)
