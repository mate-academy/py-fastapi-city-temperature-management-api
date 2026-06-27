from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from crud import get_all_cities, create_temperature
from db.engine import get_db
from temperature_fetch import fetch_temperature

app = FastAPI()


@app.get("/cities", response_model=list[schemas.CityRead])
async def get_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@app.get("/cities/{city_id}", response_model=schemas.CityRead)
async def get_one_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@app.post("/cities", response_model=schemas.CityRead)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_city(db=db, city=city)


@app.patch("/cities/{city_id}", response_model=schemas.CityRead)
async def update_city(
    city_id: int,
    city: schemas.CityPartialUpdate,
    db: AsyncSession = Depends(get_db),
):
    updated = await crud.patch_city(db=db, city_id=city_id, city=city)
    if not updated:
        raise HTTPException(status_code=404, detail="City not found")
    return updated


@app.delete("/cities/{city_id}", response_model=schemas.CityRead)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return deleted


@app.post("/temperatures/update")
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    cities = await get_all_cities(db=db)

    results = []
    for city in cities:
        temperature = await fetch_temperature(city.name)

        if temperature is None:
            continue

        record = await create_temperature(
            db=db,
            city_id=city.id,
            temperature=temperature,
        )
        results.append(record)

    return results


@app.get("/temperatures", response_model=list[schemas.TemperatureRead])
async def get_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await crud.get_temperatures(db=db, city_id=city_id)
