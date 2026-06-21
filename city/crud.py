from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) ->  list[models.City]:
    cities = await db.scalars(select(models.City))

    return cities.all()


async def create_city(db: AsyncSession, city: schemas.CityCreate) -> models.City:
    city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(select(models.City).where(models.City.id == city_id))


async def update_city(db: AsyncSession, city_update: schemas.CityCreate, city_id: int) -> models.City:
    city = await get_city_by_id(db=db, city_id=city_id)
    city.name = city_update.name
    city.additional_info = city_update.additional_info

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    city = await get_city_by_id(db=db, city_id=city_id)

    if not city:
        return False

    await db.delete(city)
    await db.commit()
    return True
