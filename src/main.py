from typing import Any, AsyncGenerator

import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src import routers


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, Any]:
    application.state.http_client = httpx.AsyncClient(
        timeout=10.0,
        headers={
            "User-Agent": "FastAPI-wttr-client/1.0"
        }
    )

    try:
        yield
    finally:
        await application.state.http_client.aclose()


app = FastAPI(lifespan=lifespan)

app.include_router(routers.city_router)
app.include_router(routers.temperature_router)
