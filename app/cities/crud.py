from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cities.models import City
from app.cities.schemas import CityCreate, CityUpdate


async def get_cities(db: AsyncSession) -> list[City]:
    stmt = select(City)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_city_by_id(db: AsyncSession, city_id: int) -> City | None:
    return await db.get(City, city_id)


async def get_city_by_name(db: AsyncSession, name: str) -> City | None:
    stmt = select(City).where(City.name == name)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_city(db: AsyncSession, city_data: CityCreate) -> City:
    city = City(
        name=city_data.name,
        latitude=city_data.latitude,
        longitude=city_data.longitude,
        additional_info=city_data.additional_info,
    )
    db.add(city)
    await db.commit()
    await db.refresh(city)
    return city


async def update_city(
    db: AsyncSession,
    city: City,
    city_data: CityUpdate
) -> City:
    for key, value in city_data.model_dump(exclude_unset=True).items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)
    return city


async def delete_city(db: AsyncSession, city: City) -> None:
    await db.delete(city)
    await db.commit()
