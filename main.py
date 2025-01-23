from fastapi import FastAPI, Depends

from database import get_db
from city_temp.city.router import router as city_router
from city_temp.temperature.router import router as temperature_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(city_router, dependencies=[Depends(get_db)])
app.include_router(temperature_router, dependencies=[Depends(get_db)])
