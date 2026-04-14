from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from city_api.models import City
from city_api.schemas import CityCreateSchema


async def create_city(data: CityCreateSchema, db: AsyncSession):
    city = City(
        name=data.name,
        additional_info=data.additional_info
    )

    db.add(city)
    await db.commit()
    await db.refresh(city)

    return city


async def get_city(db: AsyncSession):
    request = await db.execute(select(City))
    cities = request.scalars().all()

    return cities
