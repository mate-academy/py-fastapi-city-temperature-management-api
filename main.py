from fastapi import FastAPI
from database import engine, Base
import models
from cities.routes import router as city_router
from temperature.routes import router as temperature_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(city_router, prefix="/api/v1/cities", tags=["cities"])
app.include_router(temperature_router, prefix="/api/v1/temperatures", tags=["temperatures"])
