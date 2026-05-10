from fastapi import APIRouter, Depends, status
from app.schemas.city import CityCreate, CityResponse
from app.api.dependencies import get_city_service
from app.services.city_service import CityService

router = APIRouter(prefix="/cities", tags=["Cities"])


@router.get("/", response_model=list[CityResponse])
async def read_cities(service: CityService = Depends(get_city_service)):
    return await service.get_all_cities()


@router.post("/", response_model=CityResponse,
             status_code=status.HTTP_201_CREATED)
async def create_city(city: CityCreate,
                      service: CityService = Depends(get_city_service)):
    return await service.create_city(city)


@router.delete("/{city_id}")
async def delete_city(city_id: int,
                      service: CityService = Depends(get_city_service)):
    return await service.delete_city(city_id)
