from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import get_settings
from exceptions import AppException
from routers import cities, temperatures


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    get_settings()
    yield


app = FastAPI(title="City Temperature Management API", lifespan=lifespan)


@app.exception_handler(AppException)
async def exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(cities.router, prefix="/cities", tags=["Cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["Temperatures"])
