from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from datetime import datetime
import schemas
import crud
from database import engine, Base
from dependencies import get_db
import os
from fastapi import FastAPI



OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "City Temperature API is running!"}



@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    return await crud.create_city(db, city)


@app.get("/cities/", response_model=list[schemas.City])
async def read_cities(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await crud.get_cities(db, skip, limit)


@app.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db, city_id)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int, city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.update_city(db, city_id, city)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@app.delete("/cities/{city_id}")
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    db_city = await crud.delete_city(db, city_id)
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return {"message": "City deleted"}


@app.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await crud.get_cities(db)
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                OPENWEATHER_URL,
                params={
                    "q": city.name,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric",
                },
            )
            if response.status_code == 200:
                data = response.json()
                temp_value = data["main"]["temp"]

                new_temp = schemas.TemperatureCreate(
                    city_id=city.id,
                    date_time=datetime.utcnow(),
                    temperature=temp_value,
                )
                await crud.create_temperature(db, new_temp)
            else:
                print(f"Не вдалося отримати температуру для {city.name}")

    return {"message": "Temperatures updated"}


@app.get("/temperatures", response_model=list[schemas.Temperature])
async def read_temperatures(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    return await crud.get_temperatures(db, skip, limit)


@app.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures_by_city(
    city_id: int, db: AsyncSession = Depends(get_db)
):
    temps = await crud.get_temperatures_by_city(db, city_id)
    if not temps:
        raise HTTPException(
            status_code=404,
            detail="No temperature records found for this city",
        )
    return temps
