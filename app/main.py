from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.session import init_db
from routers.city import router as city_router
from routers.temperature import router as temperature_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    root_path="/api/v1",
    title="City Temperature Management API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(city_router)
app.include_router(temperature_router)
