from fastapi import FastAPI

from city import router as city_router
from temperature import router as temperature_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


app.include_router(city_router.router)
app.include_router(temperature_router.router)