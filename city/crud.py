from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city.models import CityModel
from city.schemas import CityCreateSchema


async def get_all_cities(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(CityModel).offset(skip).limit(limit).order_by(CityModel.id.desc())
    )
    cities = result.scalars().all()
    return cities


async def get_total_cities_count(db: AsyncSession):
    result = await db.execute(select(CityModel))
    return len(result.all())


async def get_city_by_id(db: AsyncSession, city_id: int):
    result = await db.execute(select(CityModel).where(CityModel.id==city_id))
    city = result.scalar_one_or_none()
    return city


async def get_city_by_name(db: AsyncSession, city_name: str):
    result = await db.execute(select(CityModel).where(CityModel.name==city_name))
    city = result.scalar_one_or_none()
    return city


async def create_city(db: AsyncSession, city_data: CityCreateSchema):
    city = CityModel(
        name=city_data.name,
        additional_info=city_data.additional_info,
    )

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def get_cities(db: AsyncSession):
    result = await db.execute(select(CityModel))
    cities = result.scalars().all()

    return cities
