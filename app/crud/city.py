from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CityAlreadyExistsError(Exception):
    pass


async def create_city(db: AsyncSession, data: CityCreate) -> City:
    city = City(
        name=data.name,
        additional_info=data.additional_info,
        latitude=data.latitude,
        longitude=data.longitude,
    )
    db.add(city)
    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise CityAlreadyExistsError("City with this name already exists") from e
    await db.refresh(city)
    return city


async def list_cities(db: AsyncSession) -> list[City]:
    res = await db.execute(select(City).order_by(City.id))
    return list(res.scalars().all())


async def get_city(db: AsyncSession, city_id: int) -> City | None:
    res = await db.execute(select(City).where(City.id == city_id))
    return res.scalar_one_or_none()


async def update_city(db: AsyncSession, city: City, data: CityUpdate) -> City:
    if data.name is not None:
        city.name = data.name
    if data.additional_info is not None:
        city.additional_info = data.additional_info
    if data.latitude is not None:
        city.latitude = data.latitude
    if data.longitude is not None:
        city.longitude = data.longitude

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise CityAlreadyExistsError("City with this name already exists") from e

    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city: City) -> None:
    await db.delete(city)
    await db.commit()
