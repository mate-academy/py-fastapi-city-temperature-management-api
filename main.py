import os
from contextlib import asynccontextmanager

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI

from cities import router as cities_router

load_dotenv()

WEATHER_API_URL = os.getenv("WEATHER_API_URL")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


@asynccontextmanager
async def lifespan(app_: FastAPI):
    client = httpx.AsyncClient()
    app_.state.client = client
    yield
    await client.aclose()


app = FastAPI(lifespan=lifespan)


def get_http_client() -> httpx.AsyncClient:
    return app.state.client


app.include_router(cities_router.router)
