from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import (
    CommonDB,
    CommonLimitation
)

from city import schemas, crud
from city.dependencies import (
    CommonParametersWithId,
)


router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(
        params_db: CommonDB,
        params_limit: CommonLimitation
):
    return await crud.get_all_cites(db=params_db, **params_limit)


@router.get("/cities/{city_id}", response_model=schemas.CityDetail)
async def get_city_by_id(
        params_db: CommonDB,
        params_id: CommonParametersWithId
):
    city = await crud.get_city_by_id(db=params_db, city_id=params_id)

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City doesn't exist"
        )

    return city


@router.post("/cities/", response_model=schemas.City)
async def post_city(
        city: schemas.CityCreate,
        params_db: CommonDB
):
    city = await crud.post_city(db=params_db, city=city)

    if city is None:
        raise HTTPException(
            status_code=400,
            detail="City with this name already exist"
        )
    return city


@router.put("/cities/{city_id}", response_model=schemas.CityDetail)
async def put_city(
        updated_city: schemas.CityUpdate,
        params_id: CommonParametersWithId,
        params_db: CommonDB
):
    city = await crud.update_city(
        db=params_db,
        city_id=params_id,
        updated_city=updated_city
    )

    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City doesn't exist"
        )

    return city


@router.delete("/cities/{city_id}", response_model=schemas.CityDetail)
async def delete_city(
        params_id: CommonParametersWithId,
        params_db: CommonDB
):
    city = await crud.delete_city(db=params_db, city_id=params_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City doesn't exist")
    return city
