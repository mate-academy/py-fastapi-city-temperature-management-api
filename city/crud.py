from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, models


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate,
) -> models.City:
    city = models.City(
        **city.model_dump()
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city

async def get_city_list(
        db: AsyncSession
) -> list[models.City]:
    city_list = (await db.scalars(select(models.City))).all()
    return list(city_list)

async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.City | None:
    stmt = select(models.City).where(models.City.id == city_id)
    city = await db.scalar(stmt)
    return city


async def delete_city_by_id(
        db: AsyncSession,
        city_id: int
) -> bool:
    stmt = delete(models.City).where(models.City.id == city_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def update_city_by_id(
        db: AsyncSession,
        city_id: int,
        city_data: schemas.CityUpdate
) -> models.City | None:

    stmt = (update(models.City)
            .where(models.City.id == city_id)
            .values(
                **city_data.model_dump()
            )
            .returning(models.City)
            )

    city = await db.scalar(stmt)
    await db.commit()
    return city
