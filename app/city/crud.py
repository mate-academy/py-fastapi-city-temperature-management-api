from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City
from app.city.schemas import CityCreateModel


async def get_city_list(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())


async def get_city_by_id(db: AsyncSession, id_: int) -> City | None:
    result = await db.scalars(select(City).where(City.id == id_))
    return result.one_or_none()


async def create_city(db: AsyncSession, data: CityCreateModel) -> City:
    result = insert(City).values(**data.model_dump())

    city = await db.scalar(result)
    await db.commit()
    await db.refresh(city)

    return city
