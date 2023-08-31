from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import (
    DB,
    Pagination
)

from city import schemas, crud


router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(db: DB,
                     pagination: Pagination):
    return await crud.get_all_cities(db=db, **pagination)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def get_city_by_id(db: DB,
                         city_id: int):
    city = await crud.get_city_by_id(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City doesn't exist"
        )

    return city


@router.post("/cities/", response_model=schemas.City)
async def post_city(db: DB,
                    city: schemas.CityCreate):
    city = await crud.post_city(db=db, city=city)

    if city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exist"
        )
    return city


@router.put("/cities/{city_id}/", response_model=schemas.CityDetail)
async def put_city(db: DB,
                   city_id: int,
                   updated_city: schemas.CityUpdate):
    city = await crud.update_city(
        db=db,
        city_id=city_id,
        updated_city=updated_city
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City doesn't exist"
        )

    return city


@router.delete("/cities/{city_id}/", response_model=schemas.CityDetail)
async def delete_city(db: DB,
                      city_id: int):
    city = await crud.delete_city(db=db, city_id=city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City doesn't exist")
    return city
