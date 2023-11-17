from typing import Any, Sequence

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas
from city.models import City


async def get_all_cities(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> Sequence[City | Any]:
    query = select(City).offset(skip).limit(limit)
    city_list = await db.execute(query)
    return city_list.scalars().all()


async def get_city(db: AsyncSession, city_id: int) -> City | Any:
    query = select(City).where(City.id == city_id)
    response = await db.execute(query)
    city = response.scalars().first()

    if city is None:
        raise HTTPException(
            status_code=404,
            detail=f"The city with id {city_id} does not exist"
        )

    return city


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreateSerializer
) -> dict:
    query = insert(City).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}

    return response


async def update_city(
        db: AsyncSession,
        city_data: schemas.CityBaseSerializer,
        city_id: int
) -> City:
    db_city = await get_city(db=db, city_id=city_id)
    for attr, value in city_data.model_dump().items():
        setattr(db_city, attr, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> HTTPException:
    db_city = await get_city(db, city_id=city_id)
    await db.delete(db_city)
    await db.commit()
    return HTTPException(
            status_code=200,
            detail=f"City with id {city_id} has been deleted"
    )
