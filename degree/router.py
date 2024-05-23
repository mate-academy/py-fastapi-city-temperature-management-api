from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

import city_data.crud as city_crud
from dependencies import get_db
from . import schemas, crud

router = APIRouter()


@router.get("/temperatures/?city_id={city_id}",
            response_model=list[schemas.Temperature])
@router.get("/temperatures/", response_model=list[schemas.Temperature])
async def get_degree_list(skip: int = 0, limit: int = 10,
                          db: AsyncSession = Depends(get_db),
                          city_id: int | None = None) -> list | None:
    if city_id is None:
        db_record = await crud.get_all_degrees(db=db, skip=skip, limit=limit)
        if not db_record:
            raise HTTPException(
                status_code=404,
                detail="No temperatures in database"
            )
    else:
        db_record = await city_crud.get_city_by_id(db=db, city_id=city_id)
        if db_record is None:
            raise HTTPException(
                status_code=404,
                detail=f"No city with id='{city_id}' found in database"
            )
        db_record = await crud.get_degrees_by_city_id(
            db=db, city_id=city_id, skip=skip, limit=limit
        )
        if not db_record:
            raise HTTPException(
                status_code=404,
                detail="No temperatures in database"
            )

    return db_record


@router.post("/temperatures/update/{city_name}")
async def update_degree_by_city_name(
        city_name: str,
        db: AsyncSession = Depends(get_db)
):
    city = await city_crud.get_city_by_name(db=db, name=city_name)
    if city is None:
        raise HTTPException(
            status_code=404,
            detail=f"City '{city_name.capitalize()}' not found in database"
        )
    db_record = await crud.update_degree_by_city(
        db=db, city_name=city.name, city_id=city.id
    )
    return db_record


@router.delete("/temperatures/{city_id}")
async def del_degrees_by_city_id(
        city_id: int, db: AsyncSession = Depends(get_db)
) -> dict | None:
    db_record = await crud.clear_degrees_for_city_id(db=db, city_id=city_id)
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail=f"Failed to clear temperature records "
                   f"for city id = {city_id}"
        )
    return db_record


@router.delete("/temperatures/", description="Clear temperature history!")
async def del_degrees_list(db: AsyncSession = Depends(get_db)) -> dict | None:
    db_record = await crud.clear_degrees_all(db=db)
    if not db_record:
        raise HTTPException(
            status_code=404,
            detail='Failed to clear temperature records'
        )
    return db_record


@router.post("/temperatures/update/")
async def update_degree_by_all_cities(
        db: AsyncSession = Depends(get_db)
):
    city_list = await city_crud.get_all_cities(db=db, skip=0, limit=99999)
    if not city_list:
        raise HTTPException(
            status_code=404,
            detail="City list is empty"
        )
    tasks = []
    for city in city_list:
        tasks.append(crud.update_degree_by_city(
            db=db, city_name=city.name, city_id=city.id)
        )
    await asyncio.gather(*tasks)

    return "Success"
