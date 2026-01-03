import logging

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.routers import cities, temperatures
from app.database import engine, Base
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    general_exception_handler
)
from app.services.weather import close_http_client

logger = logging.getLogger(__name__)

app = FastAPI(
    title="City Temperature Management API",
    description="API for managing city data and their temperatures",
    version="1.0.0"
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(cities.router, prefix="/cities", tags=["cities"])
app.include_router(temperatures.router, prefix="/temperatures", tags=["temperatures"])


app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("shutdown")
async def shutdown():
    await close_http_client()
