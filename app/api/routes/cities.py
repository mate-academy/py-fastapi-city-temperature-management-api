from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession

from dependecies import get_db
import crud.city as crud_city
import schemas


router = APIRouter()


async def common_parameters(city_id: int,  db: AsyncSession = Depends(get_db)):
    return {"city_id": city_id, "db": db}


CommonsDep = Annotated[dict, Depends(common_parameters)]


@router.post("/cities/", response_model=schemas.City)
async def create_city(
    city: schemas.CityCreate,
    db: AsyncSession = Depends(get_db)
):
    return await crud_city.create_city(db=db, city=city)


@router.get("/cities/", response_model=list[schemas.City])
async def read_cities(db: AsyncSession = Depends(get_db)):
    cities = await crud_city.get_all_cities(db=db)

    if not cities:
        raise HTTPException(
            status_code=404,
            detail="No cities found."
        )

    return cities


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_single_city(commons: CommonsDep):
    city = await crud_city.get_single_city(
        db=commons["db"],
        city_id=commons["city_id"]
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail=f"City with id {commons['city_id']} not found."
        )

    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def city_update(
    city: schemas.CityUpdate,
    commons: CommonsDep
):
    return await crud_city.update_city(
        city=city,
        db=commons["db"],
        city_id=commons["city_id"]
    )


@router.delete("/cities/{city_id}/", response_model=schemas.CityDelete)
async def city_delete(commons: CommonsDep):
    result = await crud_city.remove_city(
        db=commons["db"],
        city_id=commons["city_id"]
    )
    return result
