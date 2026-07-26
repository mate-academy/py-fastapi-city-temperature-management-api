from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from city import schemas, crud
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/cities/", response_model=list[schemas.City])
async def read_all_cities(
    db: SessionDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    return await crud.get_city_list(db=db, limit=limit, skip=skip)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(db: SessionDep, city_id: int):
    city = await crud.get_city(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(status_code=400, detail="City not found")
    return city


@router.post("/cities/", response_model=schemas.City)
async def update_city(db: SessionDep, city: schemas.CreateUpdateCity):
    city_db = await crud.get_city_by_name(db=db, city_name=city.name)
    if city_db:
        raise HTTPException(status_code=400, detail="Such name for City already exists")
    return await crud.create_city(db=db, city=city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(db: SessionDep, city_id: int, city: schemas.CreateUpdateCity):
    city_by_id = await crud.get_city(db=db, city_id=city_id)
    if city_by_id is None:
        raise HTTPException(status_code=400, detail="City not found")

    city_by_name = await crud.get_city_by_name(db=db, city_name=city.name)
    if city_by_name and city_by_name.id != city_id:
        raise HTTPException(status_code=400, detail="Such name for City already exists")
    return await crud.update_city(db=db, city_id=city_id, city=city)


@router.delete("/cities/{city_id}/")
async def read_city(db: SessionDep, city_id: int):
    city_by_id = await crud.get_city(db=db, city_id=city_id)
    if city_by_id is None:
        raise HTTPException(status_code=400, detail="City not found")
    await crud.delete_city(db=db, city_id=city_id)
