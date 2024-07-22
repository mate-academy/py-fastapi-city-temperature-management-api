from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas


async def get_cities(db: AsyncSession) -> list[models.City]:
    list = await db.execute(select(models.City))

    return list.scalars().all()


async def get_city(db: AsyncSession, city_id: int) -> models.City | None:
    city = await db.execute(
        select(models.City)
        .where(models.City.id == city_id)
    )

    return city.scalar()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.City:
    result = await db.execute(
        insert(models.City)
        .values(
            name=city.name,
            additional_info=city.additional_info
        )
    )

    await db.commit()

    return {**city.model_dump(), "id": result.lastrowid}


async def update_city(
        db: AsyncSession,
        city_id: int,
        new_city: schemas.CityUpdate
) -> models.City:
    await db.execute(
        update(models.City)
        .where(models.City.id == city_id)
        .values(**new_city.dict())
    )

    await db.commit()

    city = await get_city(db=db, city_id=city_id)

    return city


async def delete_city(db: AsyncSession, city_id: int) -> None:
    await db.execute(
        delete(models.City)
        .where(models.City.id == city_id)
    )

    await db.commit()
