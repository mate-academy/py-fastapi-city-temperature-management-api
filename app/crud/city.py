from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.services.get_lat_and_lon import get_lat_and_lon


async def get_cities_list(db: AsyncSession) -> list[models.DBCity]:
    result = await db.execute(select(models.DBCity))
    return result.scalars().all()


async def get_city_by_id(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    result = await db.execute(
        select(models.DBCity).where(models.DBCity.id == city_id)
    )
    return result.scalar_one_or_none()


async def get_city_by_name(
        db: AsyncSession,
        name: str
) -> models.DBCity | None:
    result = await db.execute(
        select(models.DBCity).where(models.DBCity.name == name)
    )
    return result.scalar_one_or_none()


async def create_city(
        db: AsyncSession,
        city: schemas.CityCreate
) -> models.DBCity:
    lat, lon = await get_lat_and_lon(city.name)

    db_city = models.DBCity(
        name=city.name,
        additional_info=city.additional_info,
        latitude=lat,
        longitude=lon,
    )
    db.add(db_city)
    await db.commit()
    await db.refresh(db_city)
    return db_city


async def update_city(
        db: AsyncSession,
        city: schemas.CityUpdate,
        city_id: int
) -> models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)

    if not db_city:
        return None

    if city.name is not None:
        db_city.name = city.name

        lat, lon = await get_lat_and_lon(city.name)
        db_city.latitude = lat
        db_city.longitude = lon

    if city.additional_info is not None:
        db_city.additional_info = city.additional_info

    await db.commit()
    await db.refresh(db_city)
    return db_city


async def delete_city(
        db: AsyncSession,
        city_id: int
) -> models.DBCity | None:
    db_city = await get_city_by_id(db, city_id)

    if not db_city:
        return None

    await db.delete(db_city)
    await db.commit()
    return db_city
