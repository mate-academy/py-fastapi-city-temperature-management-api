from fastapi import FastAPI
from database import get_db, Base
from city.router import city_routers
from temperature.router import temp_routers


app = FastAPI()


app.include_router(city_routers.city_router, prefix="/cities", tags=["cities"])
app.include_router(temp_routers.temperature_router, prefix="/temperatures", tags=["temperatures"])


@app.get("/")
async def read_root():
    return {"Hello": "World"}
