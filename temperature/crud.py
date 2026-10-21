from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from temperature import models
from temperature.models import DBTemperature


async def get_all_temperatures(db: AsyncSession) -> list[models.DBTemperature]:
    temps = await db.scalars(select(models.DBTemperature).options(selectinload(DBTemperature.city)))
    return temps.all()
