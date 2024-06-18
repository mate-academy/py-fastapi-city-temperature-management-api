from fastapi import FastAPI
from database import init_db, database
from city import router as city_router
from temperature import router as temperature_router

app = FastAPI()

app.include_router(city_router.router, prefix="/city", tags=["cities"])
app.include_router(temperature_router.router, prefix="/temperature", tags=["temperatures"])


@app.on_event("startup")
async def startup() -> None:
    await database.connect()
    await init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
