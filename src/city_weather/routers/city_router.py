from fastapi import APIRouter
from typing import List
from fastapi import Depends
from src.city_weather.db_managers.city_manager import CityDBManager
from src.city_weather.schemas import CityCreate, City
from src.dependencies import get_city_manager


city_router = APIRouter(tags=["Cities"], prefix="/cities")


@city_router.get("/", response_model=List[City])
async def retrieve_cities(manager: CityDBManager = Depends(get_city_manager)):
    return await manager.get_list_of_items()


@city_router.post("/")
async def retrieve_cities(city: CityCreate, manager: CityDBManager = Depends(get_city_manager)):
    return await manager.create_new_item(data=city)


@city_router.get("/{city_id}/", response_model=City)
async def retrieve_cities(city_id: int, manager: CityDBManager = Depends(get_city_manager)):
    return await manager.get_item_by_id(city_id)


@city_router.put("/", response_model=City)
async def retrieve_cities(city: City, manager: CityDBManager = Depends(get_city_manager)):
    return await manager.update_item(data=city)


@city_router.delete("/{city_id}/")
async def retrieve_cities(city_id: int, manager: CityDBManager = Depends(get_city_manager)):
    return await manager.delete_item(city_id)
