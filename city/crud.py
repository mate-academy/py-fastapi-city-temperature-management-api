from typing import Optional, Any, Sequence
from sqlalchemy import select, Row, RowMapping, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_all_cities(
        db: AsyncSession
) -> Sequence[Row | RowMapping | Any]:
    query = select(models.City)
    result = await db.execute(query)
    city_list = result.scalars().all()
    return city_list


async def create_city(
        db: AsyncSession, city: schemas.CityCreate
) -> dict[str, Any]:
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def get_city_by_id(
        db: AsyncSession, city_id: int
) -> Optional[models.City]:
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    city = result.scalars().first()
    return city


async def update_city(
        db: AsyncSession, city_id: int, city: dict
) -> Optional[models.City]:
    query = update(models.City).where(models.City.id == city_id).values(**city)
    await db.execute(query)
    await db.commit()
    query = select(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    updated_city = result.scalars().first()
    return updated_city


async def delete_city(db: AsyncSession, city_id: int) -> dict:
    query = delete(models.City).where(models.City.id == city_id)
    await db.execute(query)
    await db.commit()
    return {"message": f"City with id {city_id} has been deleted."}
