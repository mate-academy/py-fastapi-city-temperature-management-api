from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_city(db: AsyncSession):
    query = select(models.CityModels)
    city_list = await db.execute(query)
    return [city[0] for city in city_list.fetchall()]


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.CityModels).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.CityModels).where(models.CityModels.id == city_id)
    city = await db.execute(query)
    return city.scalar()


async def update_city(db: AsyncSession, city_id: int, city_data: schemas.CityCreate):
    query = (
        update(models.CityModels)
        .where(models.CityModels.id == city_id)
        .values(
            name=city_data.name,
            additional_info=city_data.additional_info,
        )
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return {"message": "City updated successfully"}


async def delete_city(db: AsyncSession, city_id: int):
    query = (
        delete(models.CityModels)
        .where(models.CityModels.id == city_id)
        .execution_options(synchronize_session="fetch")
    )
    await db.execute(query)
    await db.commit()
    return {"message": "City deleted successfully"}
