from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.City]:
    cities = await db.scalars(select(models.City))

    return cities.all()


async def get_city_by_name(db: AsyncSession, name: str) -> models.City | None:
    return await db.scalar(
        select(
            models.City
        ).where(
            models.City.name == name
        )
    )


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.City | None:
    return await db.scalar(
        select(
            models.City
        ).where(
            models.City.id == city_id
        )
    )


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)

    return db_city
