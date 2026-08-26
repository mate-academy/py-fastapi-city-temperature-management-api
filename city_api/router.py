from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import crud, schemas
from dependencies import get_db


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities_list(db: Annotated[AsyncSession, Depends(get_db)]):
    return await crud.get_all_cities(db)


@router.get(
    "/cities/{city_id}/",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
)
async def get_city_by_id(city_id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return db_city


@router.get(
    "/cities//by-name/{name}/",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
)
async def get_city_by_name(name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    db_city = await crud.get_city_by_name(db=db, city_name=name)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    return db_city


@router.post(
    "/cities/",
    response_model=schemas.City,
    status_code=status.HTTP_201_CREATED,
)
async def create_city(
        city: schemas.CityCreate,
        db: Annotated[AsyncSession, Depends(get_db)],
):
    db_city = await crud.get_city_by_name(db=db, city_name=city.name)

    if db_city:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="City already exists",
        )

    try:
        return await crud.create_city(db=db, city=city)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.patch(
    "/cities/{city_id}/",
    response_model=schemas.City,
    status_code=status.HTTP_200_OK,
)
async def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: Annotated[AsyncSession, Depends(get_db)],
):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    try:
        return await crud.update_city(
            db=db,
            db_city=db_city,
            city_update=city_update
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.delete("/cities/{city_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(db: Annotated[AsyncSession, Depends(get_db)], city_id: int):
    db_city = await crud.get_city_by_id(db=db, city_id=city_id)
    if db_city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found",
        )

    await crud.delete_city(db=db, db_city=db_city)
