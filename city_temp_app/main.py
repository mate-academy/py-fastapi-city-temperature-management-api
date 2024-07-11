from fastapi import FastAPI
from city_temp_app.api import city, temperature
from city_temp_app.database import engine, Base


app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as start_engine:
        await start_engine.run_sync(Base.metadata.create_all)

app.include_router(city.router, prefix="/cities", tags=["cities"])
app.include_router(
    temperature.router, prefix="/temperatures", tags=["temperatures"]
)
