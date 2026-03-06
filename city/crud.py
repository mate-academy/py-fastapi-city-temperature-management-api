from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import City
from city.schemas import CityCreate, CityUpdate, CityRead


async def get_all_cities(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
):
    stmt = (
        select(City).offset(skip).limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_city(db: AsyncSession, city_in: CityCreate) -> CityRead:
    city = City(name=city_in.name, additional_info=city_in.additional_info)
    db.add(city)
    await db.commit()
    await db.refresh(city)

    return CityRead(
        id=city.id, name=city.name, additional_info=city.additional_info
    )


async def get_city(db: AsyncSession, city_id: int) -> City | None:
    stmt = select(City).where(City.id == city_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_city_by_name(db: AsyncSession, city_name: str) -> City | None:
    stmt = select(City).where(City.name == city_name)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_city(
    db: AsyncSession, city_id: int, city_update: CityUpdate
) -> City | None:
    result = await db.execute(select(City).where(City.id == city_id))
    city = result.scalar_one_or_none()
    if city is None:
        return None

    data = city_update.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(city, key, value)

    await db.commit()
    await db.refresh(city)

    return city


async def delete_city(db: AsyncSession, city_id: int) -> bool:
    stmt = select(City).where(City.id == city_id)
    result = await db.execute(stmt)
    city = result.scalar_one_or_none()
    if city is None:
        return False

    await db.delete(city)
    await db.commit()
    return True
