from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.city.models import City


async def get_city_list(db: AsyncSession) -> list[City]:
    result = await db.scalars(select(City))
    return list(result.all())
