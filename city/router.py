from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies import get_db
from city import schemas, crud


router = APIRouter()


async def parameters(
    db: AsyncSession = Depends(get_db),
    city_id: int | None = None,
    city: schemas.CityCreate | None = None,

):
    return {
        "db": db,
        "city_id": city_id,
        "city": city,
    }


CommonsDep = Annotated[dict, Depends(parameters)]


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(commons: CommonsDep, skip: int = 0, limit: int = 5):
    return await crud.get_all_cities(
        db=commons["db"],
        skip=skip,
        limit=limit
    )


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city(commons: CommonsDep):
    db_city = await crud.get_city_by_id(
        db=commons["db"],
        id=commons["city_id"],
    )
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.post("/cities/", response_model=schemas.City)
async def create_city(commons: CommonsDep):
    db_city = await crud.get_city_by_name(
        db=commons["db"],
        name=commons["city"].name
    )
    if db_city:
        raise HTTPException(
            status_code=400, detail="Such name for City already exists"
        )
    return await crud.create_city(
        db=commons["db"],
        city=commons["city"]
    )


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(commons: CommonsDep):
    db_city = await crud.update_city(
        db=commons["db"],
        city_id=commons["city_id"],
        city=commons["city"]
    )
    if db_city is None:
        raise HTTPException(status_code=404, detail="City not found")
    return db_city


@router.delete("/cities/{city_id}/")
async def delete_city(commons: CommonsDep):
    city_id = commons["city_id"]
    deleted_city = await crud.delete_city(
        db=commons["db"],
        city_id=city_id
    )
    if deleted_city:
        return {"message": f"City with ID {city_id} deleted successfully"}
    return {"message": "City not found"}
