from typing import (
    Sequence,
    Dict
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app import (
    crud,
    models,
    schemas,
    dependencies
)

router = APIRouter()


@router.get("/temperatures/", response_model=Sequence[schemas.Temperature])
async def read_temperatures(
        service: crud.Service = Depends(dependencies.get_service)
) -> Sequence[models.Temperature]:
    temperatures = await service.get_temperatures()
    if not temperatures:
        raise HTTPException(
            status_code=404,
            detail="Temperatures were not found"
        )
    return temperatures


@router.get(
    "/temperatures/{city_id}", response_model=Sequence[schemas.Temperature]
)
async def read_temperature_by_city_id(
        city_id: int,
        service: crud.Service = Depends(dependencies.get_service)
) -> Sequence[models.Temperature]:
    temperature = await service.get_temperatures(city_id)
    if not temperature:
        raise HTTPException(
            status_code=404,
            detail="Temperatures for this city were not found",
        )
    return temperature


@router.post("/temperatures/update/", response_model=Dict)
async def update_temperatures(
        service: crud.Service = Depends(dependencies.get_service)
) -> Dict:
    await service.create_temperatures()

    return {
        "detail": "Temperatures updated"
    }