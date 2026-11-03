from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED

from city import schemas
from city import crud
from dependecies import DbSession

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def get_cities(db: DbSession):
    return await crud.get_all_cities(db)


@router.post("/cities/", response_model=schemas.City, status_code=HTTP_201_CREATED)
async def create_city(data: schemas.CityCreate, db: DbSession):
    return await crud.create_city(db=db, data=data)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def get_city_by_id(city_id: int, db: DbSession):
    city = await crud.get_city_by_id(db=db, city_id=city_id)
    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )
    return city


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
        city_id: int,
        data: schemas.CityUpdate,
        db: DbSession
):
    city = await crud.update_city(db=db, city_id=city_id, data=data)
    if city is None:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )
    return city


@router.delete("/cities/{city_id}/")
async def delete_city(city_id: int, db: DbSession):
    return await crud.delete_city(db=db, city_id=city_id)
