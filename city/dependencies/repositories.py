from fastapi import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from city.repositories.city_repository import CityRepository
from dependencies import get_session


def get_city_repository(session: AsyncSession = Depends(get_session)) -> CityRepository:
    return CityRepository(session)
