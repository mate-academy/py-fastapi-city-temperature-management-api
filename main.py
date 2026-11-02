from contextlib import asynccontextmanager

from fastapi import FastAPI

import models  # noqa: F401  (registers tables on Base.metadata)
from cities.router import router as cities_router
from database import Base, engine
from temperatures.router import router as temperatures_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="City Temperature Management API",
    description="Manage cities and keep a history of their temperatures.",
    lifespan=lifespan,
)

app.include_router(cities_router)
app.include_router(temperatures_router)


@app.get("/", include_in_schema=False)
def root():
    return {"message": "City Temperature Management API. See /docs."}
