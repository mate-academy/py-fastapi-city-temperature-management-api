from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from . import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))
    return cities.all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(select(models.City).where(models.City.id == city_id))


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    db_city = models.City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
    db: AsyncSession, city_id: int, city_data: schemas.CityCreate
) -> models.City | None:
    db_city = await get_city_by_id(db, city_id)
    if db_city:
        db_city.name = city_data.name
        db_city.additional_info = city_data.additional_info
        await db.commit()
        await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    db_city = await get_city_by_id(db, city_id)
    if db_city:
        await db.delete(db_city)
        await db.commit()
        return True
    return False
