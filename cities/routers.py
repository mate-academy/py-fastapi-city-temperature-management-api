from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from cities import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.post(
    "/cities/",
    response_model=schemas.CityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add new city",
    description=(
        f"This endpoint allows you to add a new city, by entering a city name "
        f"and additional information about it. If the city name already exists, "
        f"it will raise an error."
    ),
)
async def create_city(
    city: schemas.CityCreate, db: AsyncSession = Depends(get_db)
):
    try:
        city = await crud.create_city(db=db, city=city)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already exists",
        )

    return city


@router.get(
    "/cities/",
    response_model=list[schemas.CityResponse],
    summary="Get all cities",
    description="This endpoint allows you to retrieve all cities in DB",
)
async def city_list(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db=db)


@router.get(
    "/cities/{city_id}/",
    response_model=schemas.CityResponse,
    summary="Get a specific city",
    description=(
        f"This endpoint allows you to retrieve a specific city "
        f"by ID. It will raise an error if the city ID is invalid."
    ),
)
async def city_detail(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(city_id=city_id, db=db)

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return city


@router.put(
    "/cities/{city_id}/",
    response_model=schemas.CityResponse,
    summary="Update a specific city",
    description=f"This endpoint allows you to update additional information about a specific city.",
)
async def update_city(
    city_id: int,
    city_update: schemas.CityUpdate,
    db: AsyncSession = Depends(get_db),
):
    updated_city = await crud.update_city(
        db=db, city_id=city_id, city_update=city_update
    )

    if updated_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return updated_city


@router.delete(
    "/cities/{city_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a specific city",
    description=f"This endpoint allows you to delete a specific city.",
)
async def delete_city(city_id: int, db: AsyncSession = Depends(get_db)):
    success = await crud.delete_city(db=db, city_id=city_id)

    if success is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return
