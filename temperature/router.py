from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from city.crud import get_all_cities_dict
from dependencies import get_db
from temperature import schemas, crud
from temperature.requests import fetch_temperature

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
async def get_all_temperatures(db: AsyncSession = Depends(get_db), city_id: int = None):
    return await crud.get_all_temperatures(db, city_id=city_id)


@router.post("/temperatures/update/", response_model=schemas.TemperatureUpdate)
async def update_temperatures(db: AsyncSession = Depends(get_db)):
    result = {
        "succeeded": [],
        "failed": [],
    }
    cities = await get_all_cities_dict(db)
    for city in cities:
        name = city["name"]
        city_id = city["id"]
        try:
            res = await fetch_temperature(name, city_id)
        except HTTPException as e:
            result["failed"].append(
                schemas.TemperatureFailed(
                    city=name,
                    status_code=e.status_code,
                )
            )
            continue
        created = await crud.create_temperature(db, schemas.TemperatureCreate(**res))
        result["succeeded"].append(
            schemas.TemperatureSucceeded(
                city=name,
                temperature=created[0],
                date_time=created[1],
            )
        )
    return result
