from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud.city import CityService
from src.database.sqlite_db import get_sqlite_db
from src.schemas.city import CityRequestSchema, CityResponseSchema, CityTemperatureResponseSchema
from src.schemas.temperature import MessageResponseSchema

router = APIRouter()


def get_city_service(db: AsyncSession = Depends(get_sqlite_db)):
    return CityService(db)


@router.post("/fetch_ukraine_cities")
async def fetch_ukraine_cities(city_service: CityService = Depends(get_city_service)):
    await city_service.fetch_and_save_ukraine_cities()
    return MessageResponseSchema(message="Cities fetched successfully")


@router.post("/cities", response_model=CityTemperatureResponseSchema)
async def create_city(
    city_data: CityRequestSchema,
    city_service: CityService = Depends(get_city_service)
):
    return await city_service.create_city(city_data)


@router.get("/cities", response_model=list[CityTemperatureResponseSchema])
async def get_cities(city_service: CityService = Depends(get_city_service)):
    return await city_service.get_cities()


@router.get("/cities/{city_id}", response_model=CityTemperatureResponseSchema)
async def get_city(city_id: int, city_service: CityService = Depends(get_city_service)):
    return await city_service.get_city(city_id)


@router.put("/cities/{city_id}", response_model=CityResponseSchema)
async def update_city(
    city_id: int,
    city_data: CityRequestSchema,
    city_service: CityService = Depends(get_city_service)
):
    return await city_service.update_city(city_id, city_data)


@router.delete("/cities/{city_id}", response_model=CityResponseSchema)
async def delete_city(city_id: int, city_service: CityService = Depends(get_city_service)):
    return await city_service.delete_city(city_id)
