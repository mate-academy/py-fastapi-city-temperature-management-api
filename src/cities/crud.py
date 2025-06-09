from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from src.cities import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.City)
    cities_list = await db.execute(query)
    return [city[0] for city in cities_list.fetchall()]


async def create_new_city(db: AsyncSession, city: schemas.CityNew):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    new_id = result.inserted_primary_key[0] 
    response = {**city.model_dump(), "id": new_id}
    return response
   

async def get_city_by_id(db:AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def delete_city_by_id(db: AsyncSession, city_id: int):
    exists_city = await get_city_by_id(db=db, city_id=city_id)
    if exists_city:
        await db.delete(exists_city)
        await db.commit()


async def update_city_by_id(db: AsyncSession, city_id: int, update_data: schemas.CityNew):
    exists_city = await get_city_by_id(db=db, city_id=city_id)
    if exists_city:
        if update_data.name:
            exists_city.name = update_data.name 
        if update_data.additional_info:
            exists_city.additional_info = update_data.additional_info
    await db.commit()
    await db.refresh(exists_city)
    return exists_city


async def get_city_by_name(db:AsyncSession, name: str):
    query = select(models.City).where(models.City.name == name)
    result = await db.execute(query)
    return result.scalar_one_or_none()
