from fastapi import FastAPI

from city.router import router as city_router
from temperature.router import router as temperature_router

app = FastAPI(
    title="City Temperature Management API",
    description="API для керування температурними даними міст",
    version="1.0.0",
)

# Підключаємо роутери
app.include_router(city_router)
app.include_router(temperature_router)


@app.get("/")
async def root():
    return {"message": "City Temperature Management API"}
