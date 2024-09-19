from fastapi import Depends
from temperature.repositories.temperature_repository import TemperatureRepository
from temperature.dependencies.repositories import get_temperature_repository
from temperature.services.temperature_service import TemperatureService


def get_temperature_service(
    repository: TemperatureRepository = Depends(get_temperature_repository)
):
    return TemperatureService(repository)
