import asyncio

from fastapi import APIRouter
from sqlalchemy import select

from app import schemas, crud, models
from app.dependencies import DBDep
from app.services.get_weather import get_weather

router = APIRouter()


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures(db: DBDep, city_id: int | None = None):
    return await crud.get_temperatures_list(
        db=db,
        city_id=city_id
    )


@router.post("/temperatures/update/", response_model=list[schemas.Temperature])
async def update_temperature(db: DBDep):
    result = await db.execute(select(models.DBCity))
    cities = result.scalars().all()

    tasks = [get_weather(city.latitude, city.longitude) for city in cities]
    temperatures = await asyncio.gather(*tasks)

    created = []

    for city, temperature in zip(cities, temperatures):
        db_temperature = await crud.create_temperature(
            db=db,
            city_id=city.id,
            temperature=temperature
        )

        created.append(db_temperature)

    await db.commit()

    return created
