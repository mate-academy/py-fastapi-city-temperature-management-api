from fastapi import APIRouter

from dependecies.database import DataBaseDependency
from schemes.city import CityCreate, CityDetail, CityUpdate
from services.city import change_city, create_city, get_all_cities, remove_city

city = APIRouter(tags=["сity"])


@city.post("/cities", response_model=CityDetail)
async def post_city(db: DataBaseDependency, city: CityCreate):
    return await create_city(db=db, city=city)


@city.get("/cities")
async def list_cities(db: DataBaseDependency):
    return await get_all_cities(db=db)


@city.put("/cities/{city_id}", response_model=CityDetail)
async def update_city(db: DataBaseDependency, city_id: int, city: CityUpdate):
    return await change_city(db=db, city_id=city_id, city=city)


@city.delete("/cities/{city_id}")
async def delete_city(db: DataBaseDependency, city_id: int):
    return await remove_city(db=db, city_id=city_id)
