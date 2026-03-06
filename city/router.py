from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from city import crud
from city.schemas import CityRead, CityCreate, CityUpdate
from dependencies import get_db, Pagination, pagination_params

router = APIRouter()


@router.get("/cities", response_model=list[CityRead])
async def list_cities(
    db: Annotated[AsyncSession, Depends(get_db)],
    pagination: Annotated[Pagination, Depends(pagination_params)],
) -> list[CityRead]:
    return await crud.get_all_cities(
        db=db, skip=pagination.skip, limit=pagination.limit
    )


@router.post("/cities", response_model=CityRead)
async def create_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_in: CityCreate,
):
    existing_city = await crud.get_city_by_name(db=db, city_name=city_in.name)
    if existing_city:
        raise HTTPException(
            status_code=400, detail=f"City with name {city_in.name} already exists"
        )

    return await crud.create_city(db=db, city_in=city_in)


@router.get("/cities/{city_id}", response_model=CityRead)
async def read_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
):
    city = await crud.get_city(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.patch("/cities/{city_id}", response_model=CityRead)
async def update_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
    city_in: CityUpdate,
):
    try:
        city = await crud.update_city(db=db, city_id=city_id, city_update=city_in)
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail=f"City with name {city_in.name} already exists"
        )

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.delete("/cities/{city_id}", status_code=204)
async def delete_city(
    db: Annotated[AsyncSession, Depends(get_db)],
    city_id: int,
):
    deleted = await crud.delete_city(db=db, city_id=city_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")
    return None
