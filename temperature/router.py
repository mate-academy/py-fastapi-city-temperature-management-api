import asyncio

import aiohttp

from fastapi import HTTPException
from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from dependencies import get_db

from temperature import schemas, crud
from city.crud import (
    get_city,
    get_all_cities,
    update_cities_temperature
)

router = APIRouter()

API_KEY = "bff8d32b314b46069b7210605251501"


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature]
)
async def read_temperatures(db: Session = Depends(get_db), city_id: int = None):
    city = await get_city(db, city_id)

    if city is None:
        raise HTTPException(
            status_code=400, detail="City not exist"
        )

    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post("/temperatures/", response_model=schemas.Temperature)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: Session = Depends(get_db)
):
    db_temperature = await crud.get_temperature_by_city_id(
        db=db, city_id=temperature.city_id
    )
    city = await get_city(db=db, city_id=temperature.city_id)

    if city is None:
        raise HTTPException(
            status_code=400, detail="City not exist"
        )
    if db_temperature:
        raise HTTPException(
            status_code=400, detail="Temperature for city already exists"
        )

    result = await crud.create_temperature(
        db=db,
        temperature=temperature
    )
    return result


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperature(db: Session = Depends(get_db)):
    cities_temperature = {}
    cities = await get_all_cities(db=db)
    urls = [
        f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city.name}"
        for city in cities
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        results = await asyncio.gather(*tasks)

    for result in results:
        r_json = await result.json()
        city_name = r_json["location"]["name"]
        city_temperature = r_json["current"]["temp_c"]
        cities_temperature[city_name] = city_temperature

    await update_cities_temperature(db, cities_temperature)

    return await crud.get_all_temperatures(db)
