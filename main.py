from fastapi import FastAPI

from city import router as city_router
from settings import settings
from temperature import router as temperature_router

app = FastAPI(debug=settings.DEBUG)

app.include_router(city_router.router)
app.include_router(temperature_router.router)


@app.get("/")
async def root():
    return {
        "debug": settings.DEBUG,
        "database_url": settings.DATABASE_URL
    }
