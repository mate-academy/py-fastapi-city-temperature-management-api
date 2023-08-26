import asyncio

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

from temperatures import schemas, crud
from cities.crud import get_all_cities
from .temperature_getter import get_actual_temperature

router = APIRouter()


@router.get(
    "/temperatures/",
    response_model=list[schemas.Temperature],
)
async def read_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = None
) -> list[schemas.Temperature]:
    return await crud.get_all_temperatures(
        db=db,
        city_id=city_id,
    )


@router.post(
    "/temperatures/update/",
    response_model=schemas.TemperatureUpdate,
)
async def create_temperature(
    db: AsyncSession = Depends(get_db),
) -> dict:
    cities = await get_all_cities(db=db)

    await asyncio.gather(*[
        get_actual_temperature(db=db, city=city)
        for city in cities
    ])

    await db.commit()

    return {
        "message":
            "Actual temperature info for each city was added"
    }
