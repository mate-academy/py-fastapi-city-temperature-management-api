from fastapi import HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas


async def check_if_city_exists_in_db(db: AsyncSession, city_id: int) -> None:
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    if city.scalar() is None:
        raise HTTPException(status_code=404, detail="City not found")


async def get_cities(db: AsyncSession):
    result = await db.execute(select(models.City))
    return result.scalars().all()


async def get_city(db: AsyncSession, city_id: int):
    await check_if_city_exists_in_db(db=db, city_id=city_id)
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    city_data = city.scalar()
    return city_data


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.City).values(
        name=city.name, additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def update_city(
        db: AsyncSession,
        city_id: int,
        city: schemas.CityUpdate
):
    await check_if_city_exists_in_db(db=db, city_id=city_id)
    query = (
        update(models.City)
        .where(models.City.id == city_id)
        .values(
            name=city.name, additional_info=city.additional_info
        )
    )
    await db.execute(query)
    await db.commit()


async def delete_city(db: AsyncSession, city_id: int):
    db_city = await db.execute(
        select(models.City)
        .filter(models.City.id == city_id)
    )
    db_city = db_city.scalar()

    if db_city:
        await db.delete(db_city)
        await db.commit()

        return "City deleted"
