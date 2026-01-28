from fastapi import FastAPI

from app.api.routers.cities import router as cities_router
from app.api.routers.temperatures import router as temperatures_router
from app.db.session import init_db

app = FastAPI(title="City Temperature Management API")

app.include_router(cities_router, tags=["cities"])
app.include_router(temperatures_router, tags=["temperatures"])


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
