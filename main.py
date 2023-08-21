from fastapi import FastAPI

from cities.routers import router as cities_router
from temperatures.routers import router as temperatures_router

app = FastAPI()

app.include_router(cities_router, prefix="")
app.include_router(temperatures_router, prefix="")


@app.get("/")
async def root():
    return {"message": "Hello World"}
