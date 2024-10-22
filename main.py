import requests
from fastapi import FastAPI, Depends
from database.engine import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import views
import schemas

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cities", response_model=list[schemas.CityList])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await views.get_cities(db=db)


@app.post("/cities", response_model=schemas.CityList)
async def post_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await views.post_city(city=city, db=db)


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await views.delete_city(city_id=city_id, db=db)


@app.post("/temperatures/update", response_model=list[schemas.Temperature])
async def fetch_temperatures(db: AsyncSession = Depends(get_db)):
    return await views.fetch_data_temperature(db=db)


@app.get("/temperatures", response_model=list[schemas.Temperature])
async def get_temperatures(city_id: int = None, db: AsyncSession = Depends(get_db)):
    return await views.get_temperatures(city_id=city_id, db=db)
