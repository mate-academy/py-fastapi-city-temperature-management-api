from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).filter(models.DBCity.id == city_id)
    city = await db.execute(query)
    return city.first()[0]


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).filter(models.DBCity.name == name)
    city = await db.execute(query)
    return city.first()


async def update_city_by_id(db: AsyncSession, city: schemas.CityCreate, city_id: int):
    query = (
        update(models.DBCity).
        where(models.DBCity.id == city_id).
        values(name=city.name, additional_info=city.additional_info)
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": city_id}
    return resp


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city_by_id(db: AsyncSession, city_id: int):
    city = await db.get(models.DBCity, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    query = delete(models.DBCity).where(
        models.DBCity.id == city_id
    )

    await db.execute(query)
    await db.commit()

    resp = {"name": city.name, "additional_info": city.additional_info, "id": city_id}
    return resp
