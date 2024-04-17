from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import List

from city import schemas
from city.models import City


async def get_all_cites(db: AsyncSession) -> List[City]:
    query = select(City)
    cities = await db.scalars(query)
    return cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City:
    query = select(City).where(City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()
    if not city:
        raise HTTPException(
            status_code=404, detail=f"The city with id {city_id} does not exist"
        )
    return city


async def create_city(db: AsyncSession, city_data: schemas.CityBaseCreate) -> dict:
    query = insert(City).values(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city_data.model_dump(), "id": result.lastrowid}
    return response


async def update_city(db: AsyncSession, city_data: schemas.CityBase, city_id: int) -> City:
    db_city = await get_city_by_id(db, city_id=city_id)
    for attr, value in city_data.dict().items():
        setattr(db_city, attr, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> HTTPException:
    db_city = await get_city_by_id(db, city_id=city_id)
    await db.delete(db_city)
    await db.commit()
    return HTTPException(
        status_code=200, detail=f"City with id №{city_id} has been deleted."
    )
