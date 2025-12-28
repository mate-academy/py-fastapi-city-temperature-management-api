from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from cities import models
from cities import schemas


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> models.DBCity | None:
    result = await db.execute(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )
    return result.scalar_one_or_none()


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> models.DBCity | None:
    stmt = select(
        models.DBCity
    ).where(
        models.DBCity.name == name
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.DBCity:
    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        db_city: models.DBCity,
        city: schemas.CityUpdate,
) -> models.DBCity:
    for field, value in city.model_dump(exclude_unset=True).items():
        setattr(db_city, field, value)

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession,
        db_city: models.DBCity,
) -> None:
    await db.delete(db_city)
    await db.commit()
