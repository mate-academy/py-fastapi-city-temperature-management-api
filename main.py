from fastapi import FastAPI

from city.routers import router as city_router
from database import engine, Base
from temperature.routers import router as temperature_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


app.include_router(city_router, prefix="/cities", tags=["cities"])
app.include_router(temperature_router, prefix="/temperatures", tags=["temperatures"])
