from fastapi import APIRouter

from dependecies.database import DataBaseDependency
from schemes.temperature import TemperatureFilterDependency
from services.temperatures import create_temperatures, list_temperatures, update_temperatures

temperature = APIRouter(tags=["temperature"])


@temperature.get("/temperatures")
async def get_all_temperatures(
    db: DataBaseDependency, city_filter: TemperatureFilterDependency
):
    return await list_temperatures(db=db, city_filter=city_filter)


@temperature.post("/temperatures")
async def post_temperatures(db: DataBaseDependency):
    return await create_temperatures(db=db)


@temperature.patch("/temperatures")
async def patch_temperatures(db: DataBaseDependency):
    return await update_temperatures(db=db)
