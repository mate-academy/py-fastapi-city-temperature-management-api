from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from city.models import DBCity
from city import schemas


async def get_all_cities(db: AsyncSession) -> list[DBCity]:
    cities = await db.scalars(select(DBCity))
    return cities.all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> DBCity:
    db_city = DBCity(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def get_city_by_id(db: AsyncSession, city_id: int) -> DBCity | None:
    result = await db.scalars(select(DBCity).where(DBCity.id == city_id))
    return result.first()


async def update_city(
        db: AsyncSession, city_id: int, city: schemas.CityCreate
) -> DBCity | None:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return

    db_city.name = city.name
    db_city.additional_info = city.additional_info
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> bool | None:
    db_city = await get_city_by_id(db, city_id)
    if not db_city:
        return

    await db.delete(db_city)
    await db.commit()
    return True
