from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).filter(models.City.id == city_id)
    result = await db.execute(query)
    return result.first()


async def get_city_by_name(db: AsyncSession, city_name: str):
    query = select(models.City).filter(models.City.name == city_name)

    result = await db.execute(query)
    return result.first()


async def create_city(db: AsyncSession, city: schemas.CityBase):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )

    result = await db.execute(query)
    await db.commit()

    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityBase):
    db_city = await get_city_by_id(db=db, city_id=city_id)

    if db_city is not None:
        for key, value in city.model_dump().items():
            setattr(db_city, key, value)

        await db.commit()
        await db.refresh(db_city)

        return db_city


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await get_city_by_id(db=db, city_id=city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")

    await db.delete(db_city)
    await db.commit()

    return {"msg": "City deleted successfully"}
