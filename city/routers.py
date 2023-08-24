from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from city.schemas import CityBase, CityBaseCreate
from dependencies import get_db

router = APIRouter()


def parameters(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    city_data: CityBase | CityBaseCreate | None = None,
):
    return {
        "city_id": city_id,
        "db": db,
        "city_data": city_data,
    }


CommonsDep = Annotated[dict, Depends(parameters)]


@router.get("/cities", response_model=list[schemas.City])
async def read_cites(parameter: CommonsDep):
    return await crud.get_all_cites(db=parameter["db"])


@router.post("/cities", response_model=schemas.City)
async def city_create(parameter: CommonsDep):
    return await crud.create_city(db=parameter["db"], city_data=parameter["city_data"])


@router.get("/cities/{city_id}", response_model=schemas.City)
async def read_city(parameter: CommonsDep):
    return await crud.get_city_by_id(db=parameter["db"], city_id=parameter["city_id"])


@router.put("/cities/{city_id}", response_model=schemas.City)
async def update_city(parameter: CommonsDep):
    return await crud.update_city(
        db=parameter["db"],
        city_data=parameter["city_data"],
        city_id=parameter["city_id"],
    )


@router.delete("/cities/{city_id}")
async def city_delete(parameter: CommonsDep):
    return await crud.delete_city(db=parameter["db"], city_id=parameter["city_id"])
