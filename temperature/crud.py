from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import models


async def get_all_temperatures(db: AsyncSession) -> list(models.DBTemperature):
    temps = await db.scalars(select(models.DBTemperature))
    return temps.all()
