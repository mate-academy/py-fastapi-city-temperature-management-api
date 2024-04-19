from fastapi import APIRouter, HTTPException

from city import schemas, crud
from city.crud import get_city_by_name
from dependencies import CommonSession


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityList])
async def get_cities(db: CommonSession):
    return await crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.CityDetail)
async def create_city(city: schemas.CityCreate, db: CommonSession):
    if await get_city_by_name(city.name, db):
        raise HTTPException(
            status_code=400,
            detail="City with that name already exists",
        )
    return await crud.create_city(db, city)


@router.get("/cities/{city_id}/", response_model=schemas.CityDetail)
async def get_city_detail(city_id: int, db: CommonSession):
    return await crud.get_city_by_id(db, city_id)


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: CommonSession):
    city = await crud.get_city_by_id(db, city_id)
    await crud.delete_city(city, db)

    return {"message": "City deleted successfully"}


@router.put("/cities/{city_id}/", response_model=schemas.CityDetail)
async def update_city(
        city_id: int,
        city_to_update: schemas.CityCreate,
        db: CommonSession
):
    city = await crud.get_city_by_id(db, city_id)
    updated_city = await crud.update_city(db, city, city_to_update)

    return updated_city
