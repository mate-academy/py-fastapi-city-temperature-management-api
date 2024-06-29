from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def post_list_city(db: AsyncSession, city: schemas.CityBase):
    city = models.City(**city.dict())
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def get_list_city(db: AsyncSession):
    return await db.scalars(select(models.City))


async def get_detail_city(db: AsyncSession, city_pk: int):
    sql = select(models.City).filter(models.City.id == city_pk)
    city = await db.scalar(sql)
    if city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return city


async def delete_detail_city(db: AsyncSession, city_pk: int):
    await db.delete(await get_detail_city(db, city_pk))
    await db.commit()


async def update_detail_city(db: AsyncSession, city_pk: int, new_city: schemas.CityPatch):
    old_city = await get_detail_city(db, city_pk)
    for attr, value in new_city.dict(exclude_unset=True).items():
        setattr(old_city, attr, value)
    await db.commit()
    await db.refresh(old_city)
    return old_city
