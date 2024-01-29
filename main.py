from fastapi import FastAPI

from city.router import router as city_router
from temperature.routers import router as temperature_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(city_router)
app.include_router(temperature_router)
