from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()


async def create_city(db: AsyncSession, city: models.DBCity) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )

    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    result = await db.scalars(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )
    city = result.first()

    if city is not None:
        await db.delete(city)
        await db.commit()

