import asyncio

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud, utils
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        db: AsyncSession = Depends(get_db)
) -> list[schemas.City]:
    return await crud.get_all_cities(db=db)


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_single_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_id(city_id=city_id, db=db)

    if not db_city:
        raise HTTPException(status_code=404, detail="City no found")

    return db_city


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityUpdate,
        db: AsyncSession = Depends(get_db)
) -> schemas.City:
    db_city = await crud.get_city_by_id(city_id=city_id, db=db)

    if not db_city:
        raise HTTPException(status_code=404, detail="City no found")

    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}", response_model=str)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db)
) -> str:
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.delete_city(db=db, city_id=city_id)


@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def read_temperatures_by_city_id(
        city_id: int | None = None,
        db: AsyncSession = Depends(get_db)
) -> list[schemas.Temperature]:
    if not city_id:
        return await crud.get_all_temperature_records(db=db)

    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(status_code=404, detail="City not found")

    return await crud.get_temperature_record_by_city_id(
        db=db,
        city_id=city_id
    )


@router.post("/temperature/update/", response_model=list[schemas.Temperature])
async def update_temperature_by_all_cities(
        db: AsyncSession = Depends(get_db),
) -> list[schemas.Temperature]:
    cities_from_db = await read_cities(db=db)
    tasks_for_temperature = []
    async with httpx.AsyncClient() as client:
        tasks = [
            utils.get_temperature_by_api(
                city_name=city.name,
                city_id=city.id,
                client=client
            )
            for city in cities_from_db
        ]

        results = await asyncio.gather(*tasks)

        for temperature in results:
            if isinstance(temperature, schemas.TemperatureCreate):
                tasks_for_temperature.append(
                    crud.create_temperature_by_city_id(
                        temperature=temperature, db=db
                    )
                )

    all_temperatures = await asyncio.gather(*tasks_for_temperature)
    await db.commit()

    return all_temperatures
