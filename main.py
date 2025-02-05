from db.engine import create_db_and_tables
from routers.city import router as city_router
from routers.temperature import router as temperature_router

from fastapi import FastAPI


app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()


app.include_router(city_router, prefix="/cities", tags=["cities"])
app.include_router(temperature_router, prefix="/temperatures", tags=["temperatures"])
