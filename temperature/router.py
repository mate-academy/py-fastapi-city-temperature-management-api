from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from temperature import crud, schemas, models
from cities import crud as cities_crud

from db.database import get_db
from temperature.schemas import TemperatureResponse


router = APIRouter(
    prefix="/temperatures",
    tags=["Temperatures"],
)

@router.get(
    "",
    response_model=list[schemas.TemperatureResponse],
    summary="Get temperatures with pagination and city filter"
)
async def get_temperatures(
        db: AsyncSession = Depends(get_db),
        city_id: int | None = Query(None),
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=100),
) -> list[models.Temperature]:

    if city_id is not None:
        db_city = await cities_crud.get_city_by_id(
            db=db,
            city_id=city_id
        )

        if db_city is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="City not found",
            )

    return await crud.get_temperatures(
        db=db,
        city_id=city_id,
        skip=skip,
        limit=limit
    )


# Create
@router.post(
    "",
    response_model=TemperatureResponse,
    summary="Creating temperature record"
)
async def create_temperature(
        temperature: schemas.TemperatureCreate,
        db: AsyncSession = Depends(get_db)
) -> models.Temperature:

    # check city_id
    db_city = await cities_crud.get_city_by_id(
        city_id=temperature.city_id,
        db=db
    )

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"City with id {temperature.city_id} not found"
        )

    return await crud.create_temperature(
        db=db,
        temperature=temperature
    )

@router.post(
    "/update",
    response_model=list[schemas.TemperatureResponse],
    summary="Update current temperatures for cities"
)
async def update_current_temperature(
    db: AsyncSession = Depends(get_db)
) -> list[models.Temperature]:

    return await crud.update_cities_temperature(
        db=db
    )




