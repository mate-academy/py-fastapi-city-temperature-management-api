from fastapi import HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas, models


async def create_city(db: AsyncSession, city: schemas.CityIn):
    query = insert(models.City).values(
        name=city.name,
        additional_info=city.additional_info,
    )
    result = await db.execute(query)
    await db.commit()
    response = {**city.model_dump(), "id": result.lastrowid}
    return response


async def get_city_list(db: AsyncSession):
    query = select(models.City).order_by(models.City.name)
    city_list = await db.execute(query)
    return city_list.scalars().all()

async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    result = city.scalar_one_or_none()
    if result:
        return result
    raise HTTPException(status_code=404, detail="City not found")

async def update_city(db: AsyncSession,city_id: int, city: schemas.CityIn):
    query = (update(models.City).where(models.City.id == city_id).values(**city.model_dump()))
    result = await db.execute(query)
    await db.commit()
    if not result.rowcount:
        raise HTTPException(status_code=404, detail="City not found")
    query = select(models.City).where(models.City.id == city_id)
    city = await db.execute(query)
    result = city.scalar_one_or_none()
    return result

async def delete_city(db: AsyncSession, city_id: int):
    query = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(query)
    await db.commit()
    if result.rowcount:
        return None
    else:
        raise HTTPException(status_code=404, detail="City not found")
