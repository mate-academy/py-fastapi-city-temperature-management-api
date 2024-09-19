from fastapi import APIRouter, Depends, status
from city import schemas
from city.services.city_service import CityService
from city.dependencies.services import get_city_service


city_router = APIRouter()


@city_router.get("/cities/", response_model=list[schemas.City])
async def read_cities(
        city_service: CityService = Depends(get_city_service)
) -> list[schemas.City]:
    return await city_service.get_cities_list()


@city_router.post("/cities/", response_model=schemas.City, status_code=status.HTTP_201_CREATED)
async def create_city(
    city: schemas.CityCreate,
    city_service: CityService = Depends(get_city_service)
) -> schemas.City:
    return await city_service.create_city(city)


@city_router.get("/cities/{city_id}", response_model=schemas.City)
async def get_single_city(
    city_id: int,
    city_service: CityService = Depends(get_city_service)
) -> schemas.City:
    return await city_service.get_city_by_id(
        city_id
    )


@city_router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate = None,
    city_service: CityService = Depends(get_city_service)
) -> schemas.City:
    return await city_service.update_city(
        city_id, city
    )


@city_router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    city_service: CityService = Depends(get_city_service)
) -> None:
    await city_service.delete_city(city_id)
