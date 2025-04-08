from fastapi import FastAPI
from app.database import engine, Base
from app.routers import city as city_router
from app.routers import temperature as temperature_router

app = FastAPI()

app.include_router(temperature_router.router)
app.include_router(city_router.router)

@app.on_event("startup")
async def startup():
    # Запуск міграцій під час старту
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
