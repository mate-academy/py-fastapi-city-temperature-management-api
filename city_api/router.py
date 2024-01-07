from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city_api import crud
from city_api.schemas import City, CityCreate
from dependencies import get_db

router = APIRouter()


async def parameters(
    db: AsyncSession = Depends(get_db),
    city_id: int | None = None,
    city_data: CityCreate | None = None,
):
    return {
        "db": db,
        "city_id": city_id,
        "city_data": city_data,
    }


CommonsDep = Annotated[dict, Depends(parameters)]


@router.get("/cities", response_model=list[City])
async def read_cities(
    param: CommonsDep,
    skip: int = 0,
    limit: int = 5,
):
    cities = await crud.get_all_cities(db=param["db"], skip=skip, limit=limit)
    return cities


@router.get("/cities/{city_id}", response_model=City)
async def read_city(param: CommonsDep):
    city = await crud.get_city_by_id(db=param["db"], city_id=param["city_id"])
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@router.post("/cities", response_model=City)
async def create_city_endpoint(param: CommonsDep):
    db_city = await crud.get_city_by_name(
        db=param["db"], name=param["city_data"].name
    )
    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exist"
        )
    return await crud.create_city(db=param["db"], city=param["city_data"])


@router.put("/cities/{city_id}", response_model=City)
async def update_city_endpoint(param: CommonsDep):
    updated_city = await crud.update_city(
        db=param["db"],
        city_id=param["city_id"],
        city_new_data=param["city_data"],
    )
    if not updated_city:
        raise HTTPException(status_code=404, detail="City not found")
    return updated_city


@router.delete("/cities/{city_id}", response_model=dict)
async def delete_city_endpoint(param: CommonsDep):
    deleted = await crud.delete_city(db=param["db"], city_id=param["city_id"])

    if not deleted:
        raise HTTPException(status_code=404, detail="City not found")

    return {"message": "City deleted successfully"}
