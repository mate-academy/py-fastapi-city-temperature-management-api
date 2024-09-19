from fastapi import Depends

from city.repositories.city_repository import CityRepository
from city.dependencies.repositories import get_city_repository
from city.services.city_service import CityService


def get_city_service(
    city_repository: CityRepository = Depends(get_city_repository)
) -> CityService:
    return CityService(city_repository)
