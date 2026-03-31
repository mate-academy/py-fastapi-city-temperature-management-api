from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from temperature import models, schemas


async def get_all_temperatures(db: AsyncSession) -> list[models.DBTemperature]:
    temperatures = await db.scalars(select(models.DBTemperature))

    return temperatures.all()
