from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud, schemas

from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db=db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A city with this name already exists",
        )

    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city_data(
    city_id: int,
    city_data: schemas.CityCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    check_city_name = await crud.get_city_by_name(db=db, name=city_data.name)

    if (db_city.name != city_data.name) and check_city_name is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This city name is already taken.",
        )

    updated_city = await crud.update_city_data(
        db=db, city=db_city, city_data=city_data
    )

    return updated_city


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
    city_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)

    if not db_city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )

    await crud.delete_city(db=db, city=db_city)
