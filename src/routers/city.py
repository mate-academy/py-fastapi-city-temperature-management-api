from typing import List

from fastapi import APIRouter, HTTPException, Depends, Path, Query, Body
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas, dependencies
from src.cruds import city_cruds

city_router = APIRouter(prefix="/cities")


@city_router.get("", response_model=List[schemas.City])
async def get_all_cities(
        offset: int = Query(default=0),
        limit: int = Query(default=10),
        db: AsyncSession = Depends(dependencies.get_db)
) -> List[schemas.City]:
    return await city_cruds.get_all(
        offset=offset,
        limit=limit,
        db=db
    )


@city_router.get("/{city_id}", response_model=schemas.City)
async def get_by_id(
        city_id: int = Path(),
        db: AsyncSession = Depends(dependencies.get_db)
) -> schemas.City:
    city = await city_cruds.get_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(status_code=404, detail="City does not exist")

    return city


@city_router.post("", response_model=schemas.City)
async def create_city(
        city_create: schemas.CityCreate = Body(),
        db: AsyncSession = Depends(dependencies.get_db)
) -> schemas.City:
    existing_city = await city_cruds.get_by_name(name=city_create.name, db=db)

    if existing_city:
        raise HTTPException(status_code=409, detail="City with this name already exist")

    return await city_cruds.create_city(city_create=city_create, db=db)


@city_router.put("/{city_id}", response_model=None)
async def update_city(
        city_id: int = Path(),
        city_update: schemas.CityUpdate = Body(),
        db: AsyncSession = Depends(dependencies.get_db)
) -> None:
    city = await city_cruds.get_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(status_code=404, detail="City does not exist")

    return await city_cruds.update_city(
        city_id=city_id,
        city_update=city_update,
        db=db
    )


@city_router.delete("/{city_id}", response_model=None)
async def delete_city(
        city_id: int = Path(),
        db: AsyncSession = Depends(dependencies.get_db)
) -> None:
    city = await city_cruds.get_by_id(city_id=city_id, db=db)

    if not city:
        raise HTTPException(status_code=404, detail="City does not exist")

    return await city_cruds.delete_city(city_id=city_id, db=db)
