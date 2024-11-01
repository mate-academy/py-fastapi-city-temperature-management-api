from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    city_list = await db.execute(query)
    print("city_list in crud list: ", city_list)
    return [city[0] for city in city_list.fetchall()]


async def get_city_detail(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()

    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    return city


async def update_city(db: AsyncSession, city_id: int, city: schemas.CityIn):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    existing_city = result.scalars().first()

    if not existing_city:
        raise HTTPException(status_code=404, detail="City does not exist")


    existing_city.name = city.name
    existing_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(existing_city)

    return existing_city


async def delete_city(db: AsyncSession, city_id: int):
    async with db.begin():
        query = select(models.City).where(models.City.id == city_id)
        result = await db.execute(query)

        city_to_delete = result.scalar_one_or_none()
        if city_to_delete is None:
            raise HTTPException(status_code=404, detail="City was not found")

        await db.delete(city_to_delete)
        await db.commit()


async def create_city(db: AsyncSession, city: schemas.CityIn):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    results = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": results.lastrowid}
    return resp
