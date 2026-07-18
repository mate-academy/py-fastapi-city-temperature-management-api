from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from cities import crud, schemas, models
from db.database import get_db


router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.post(
    "",
    response_model=schemas.CityResponse,
    summary="Create city with parameters"
)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
) -> models.City:

    # Check double
    db_city = await crud.get_single_city_by_name(
        db=db,
        name=city.name
    )
    # raise Exception
    if db_city is not None:
        raise HTTPException(
            status_code=400,
            detail="City with such name already exists"
        )

    return await crud.create_city(
        db=db,
        city=city
    )


@router.get(
    "",
    response_model=list[schemas.CityResponse],
    summary="Get cities with pagination"
)
async def get_cities(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)
) -> list[models.City]:

    return await crud.get_cities(
        db=db,
        skip=skip,
        limit=limit
    )


@router.get(
    "/{city_id}",
    response_model=schemas.CityResponse,
    summary="Getting simple city by ID"
)
async def get_city_by_id(
    city_id: int,
    db: AsyncSession = Depends(get_db),
) -> models.City | None:
    db_city = await crud.get_city_by_id(
        db=db,
        city_id=city_id
    )
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return db_city


@router.put(
    "/{city_id}",
    response_model=schemas.CityResponse,
    summary="Update single city by ID"
)
async def update_city(
    city_id: int,
    city: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db)
) -> models.City:

    db_city = await crud.get_city_by_id(
        db=db,
        city_id=city_id
    )

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    check_db_name = await crud.get_single_city_by_name(
        db=db,
        name=city.name
    )

    if check_db_name is not None and check_db_name.id != city_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This city name is not free",
        )

    return await crud.update_city(
        db=db,
        city=city,
        db_city=db_city
    )


@router.delete(
    "/{city_id}",
    response_model=schemas.CityResponse,
    summary="Delete single city by ID"
)
async def delete_city(
        city_id: int,
        db: AsyncSession = Depends(get_db),
) -> models.City:
    db_city = await crud.get_city_by_id(
        db=db,
        city_id=city_id
    )

    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    await crud.delete_city_by_id(
        db=db,
        db_city=db_city,
    )

    return db_city
