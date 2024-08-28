from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.city import schemas


async def create_city(db: AsyncSession,
                      city: schemas.CityCreate
                      ):
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_all_city(db: AsyncSession,
                       skip: int = 0,
                       limit: int = 10
                       ):
    result = await db.execute(
        select(models.DBCity).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_city(db: AsyncSession,
                   city_id: int
                   ):
    result = await db.execute(
        select(models.DBCity).filter(models.DBCity.id == city_id)
    )
    return result.scalar()


async def update_city(db: AsyncSession,
                      city_id: int,
                      city: schemas.CityUpdate
                      ):
    await db.execute(
        update(models.DBCity)
        .where(models.DBCity.id == city_id)
        .values(name=city.name, additional_info=city.additional_info)
        .execution_options(synchronize_session="fetch")
    )
    await db.commit()

    result = await db.execute(
        select(models.DBCity).filter(models.DBCity.id == city_id)
    )
    return result.scalar()


async def delete_city(db: AsyncSession, city_id: int):
    await db.execute(
        delete(models.DBCity).where(models.DBCity.id == city_id)
    )
    await db.commit()
