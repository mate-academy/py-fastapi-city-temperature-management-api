from fastapi import FastAPI
from src.city.router import router as city_router
from src.temperature.router import router as temperature_router

app = FastAPI()
app.include_router(city_router, prefix="/api")
app.include_router(temperature_router, prefix="/api")


@app.get("/")
async def root():
    return {"result": "Hello from Yaroslav Biziuk"}
