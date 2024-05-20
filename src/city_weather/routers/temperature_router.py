from fastapi import APIRouter
from typing import List
from fastapi import Depends

from src.city_weather.db_managers.city_manager import CityDBManager
from src.city_weather.db_managers.temperature_manager import TemperatureDBManager
from src.city_weather.schemas import Temperature
from src.dependencies import get_temperature_manager, get_city_manager

temperature_router = APIRouter(tags=["Temperatures"], prefix="/temperatures")


@temperature_router.get("/", response_model=List[Temperature])
async def retrieve_temperatures(manager: TemperatureDBManager = Depends(get_temperature_manager)):
    return await manager.get_list_of_items()


@temperature_router.post("/update/")
async def retrieve_temperatures(manager: TemperatureDBManager = Depends(get_temperature_manager),
                                city_manager: CityDBManager = Depends(get_city_manager)):
    return await manager.update_item(city_manager)


@temperature_router.get("/{city_id}", response_model=List[Temperature])
async def retrieve_temperatures_by_city(city_id: int, manager: TemperatureDBManager = Depends(get_temperature_manager)):
    return await manager.get_items_by_city(city_id)
