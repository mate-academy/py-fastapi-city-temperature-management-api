from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from city import models, schemas


async def get_all_cities(db: AsyncSession) -> list[models.DBCity]:
    cities = await db.scalars(select(models.DBCity))

    return cities.all()
