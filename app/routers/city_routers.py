from typing import Sequence

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app import (
    crud,
    schemas,
    models,
    dependencies
)

router = APIRouter()


@router.get("/cities/", response_model=Sequence[schemas.City])
async def read_cities(
        service: crud.Service = Depends(dependencies.get_service)
) -> Sequence[models.City]:
    cities = await service.get_cities()
    if not cities:
        raise HTTPException(
            status_code=404,
            detail="Cites were not found"
        )
    return cities


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(
        city_id: int,
        service: crud.Service = Depends(dependencies.get_service)
) -> models.City:
    city = await service.get_city(city_id=city_id)
    if not city:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {city_id} was not found"
        )
    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
        city: schemas.CityCreate,
        service: crud.Service = Depends(dependencies.get_service)
) -> models.City:
    created_city = await service.create_city(city=city)
    if not created_city:
        raise HTTPException(
            status_code=403,
            detail="City with that name already exists"
        )
    return await service.create_city(city=city)


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(
        city_id: int,
        city: schemas.CityCreate,
        service: crud.Service = Depends(dependencies.get_service)
) -> models.City:
    city = await service.update_city(city_id=city_id, city=city)
    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City to update was not found"
        )
    return city


@router.delete("/cities/{city_id}", response_model=schemas.City)
async def delete_city(
        city_id: int,
        service: crud.Service = Depends(dependencies.get_service)
) -> models.City:
    db_city = await service.delete_city(city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=404,
            detail="City to delete was not found"
        )
    return db_city
