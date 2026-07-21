from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City


async def get_city_list(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())


async def get_city_by_id(db: AsyncSession, id_: int) -> City | None:
    result = await db.scalars(select(City).where(City.id == id_))
    return result.one_or_none()
