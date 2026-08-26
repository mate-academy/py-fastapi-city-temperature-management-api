from fastapi import FastAPI

from city_api import router as city_api
from temperature_api import router as temperature_api
app = FastAPI()

app.include_router(city_api.router)
app.include_router(temperature_api.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
