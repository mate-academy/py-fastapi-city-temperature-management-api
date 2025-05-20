from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from temperature_app.models import CityModel, TemperatureModel
from temperature_app.schemas import CityBaseSchema, TemperatureBaseSchema
from temperature_app.database import get_db
from temperature_app.crud import (create_city_in_db,
                                  get_single_city_from_db,
                                  get_all_cities_from_db,
                                  get_temperatures_from_db,
                                  create_temperature_in_db,
                                  get_temperature_by_city_id_from_db)

app = FastAPI()

@app.post("/cities/", status_code=status.HTTP_201_CREATED)
async def create_city(city_data: CityBaseSchema,
                      db: AsyncSession = Depends(get_db)):
    db_city = await create_city_in_db(db, city_data)
    return db_city


@app.get("/cities/", status_code=status.HTTP_200_OK)
async def get_all_cities(db: AsyncSession = Depends(get_db)):
    db_cities = await get_all_cities_from_db(db)
    return db_cities


@app.get("cities/{city_id}/", status_code=status.HTTP_200_OK)
async def get_single_city(city_id: int,
                          db: AsyncSession = Depends(get_db)):
    db_city = await get_single_city_from_db(db, city_id)
    if not db_city:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="City not found")
    return db_city


@app.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(city_id: int,
                      db: AsyncSession = Depends(get_db)):
    
    db_city = await get_single_city_from_db(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()


@app.post("/temperatures/", status_code=status.HTTP_201_CREATED)
async def create_temperature(temperature_data: TemperatureBaseSchema,
                             db: AsyncSession = Depends(get_db)) -> TemperatureModel:
    db_temperature = await create_temperature_in_db(db, temperature_data)
    return db_temperature


@app.get("/temperatures/{city_id}/", status_code=status.HTTP_200_OK)
async def get_temperature_by_city_id(city_id: int,
                                     db: AsyncSession = Depends(get_db)
                                     ) -> list[TemperatureModel]:
    city_exists = await get_single_city_from_db(db, city_id)
    if not city_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="City not found")
    db_temperatures = await get_temperature_by_city_id_from_db(db, city_id)
    return db_temperatures


@app.get("/temperatures/", status_code=status.HTTP_200_OK)
async def get_temperatures(db: AsyncSession = Depends(get_db)) -> list[TemperatureModel]:
    db_temperatures = await get_temperatures_from_db()
    return db_temperatures
