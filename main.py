from fastapi import FastAPI

from city import routers as city_router
from temperature import routers as temperature_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the City Temperature Management"}

app.include_router(city_router.router)
app.include_router(temperature_router.router)