from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from temperature.repositories.temperature_repository import TemperatureRepository
from dependencies import get_session


def get_temperature_repository(
    session: AsyncSession = Depends(get_session)
) -> TemperatureRepository:
    return TemperatureRepository(session)
