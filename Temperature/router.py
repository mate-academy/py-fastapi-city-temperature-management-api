import asyncio
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from City.crud import get_all_city
from Temperature import schemas, crud
from Temperature.models import DBTemperature
from dependencies import get_db
from service import fetch_weather

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(
        city_id: int | None,
        db: Annotated[AsyncSession, Depends(get_db)]
    ) -> list[schemas.Temperature]:
    return await crud.get_temperatures_list(db=db, city_id=city_id)


@router.post("/temperatures/update")
async def create_temperatures(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    cities = await get_all_city(db=db)
    tasks = [fetch_weather(city.name) for city in cities]
    results = await asyncio.gather(*tasks)
    to_create = []
    for city, weather in zip(cities, results):
        if weather is not None:
            to_create.append(DBTemperature(city_id=city.id, temperature=weather["temperature"]))
    await crud.create_temperature(db=db, temperatures=to_create)
    return {"status": "ok", "updated_count": len(to_create)}
