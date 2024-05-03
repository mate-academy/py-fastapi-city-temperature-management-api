from typing import List

from fastapi import APIRouter, HTTPException

from city import schemas, crud
from city.dependencies import CommonParametersWithId
from dependencies import CommonDB, CommonLimitation

router = APIRouter()


@router.get("/cities/", response_model=List[schemas.City])
async def get_cities(params_db: CommonDB, params_limit: CommonLimitation):
    return await crud.get_cities(db=params_db, **params_limit)


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, params_db: CommonDB):
    city = await crud.post_city(db=params_db, city=city)

    if city is None:
        raise HTTPException(status_code=400, detail="Such name for City already exists")

    return city


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def get_city(params_db: CommonDB, params_id: CommonParametersWithId):
    city = await crud.get_city_by_id(db=params_db, city_id=params_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.put("/cities/{city_id}/", response_model=schemas.CityDetail)
async def update_city(
    updated_city: schemas.CityUpdate,
    params_db: CommonDB,
    params_id: CommonParametersWithId,
):
    city = await crud.update_city(
        db=params_db, city_id=params_id, updated_city=updated_city
    )

    if city is None:
        raise HTTPException(status_code=404, detail="City not found")

    return city


@router.delete("/cities/{city_id}/", response_model=schemas.CityDetail)
async def delete_city(params_id: CommonParametersWithId, params_db: CommonDB):
    city = await crud.delete_city(db=params_db, city_id=params_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City does`t exist")
    return city
