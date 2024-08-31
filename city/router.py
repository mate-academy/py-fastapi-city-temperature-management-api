from fastapi import APIRouter

from dependencies import CommonDB, CommonLimits
from . import crud, schemas


router = APIRouter()


@router.get("/cities/", response_model=list[schemas.CityIn])
async def list_of_all_cities(db: CommonDB, limits: CommonLimits) -> list[schemas.City]:
    return await crud.get_all_cities(db=db, **limits)


@router.post("/cities/", response_model=schemas.City)
async def add_city(city: schemas.CityIn, db: CommonDB) -> schemas.City:
    return await crud.create_city(db=db, city=city)


@router.get("/cities/{city_id}/", response_model=schemas.CityIn)
async def get_city_by_id(city_id: int, db: CommonDB) -> schemas.CityIn:
    return await crud.get_city(db=db, city_id=city_id)


@router.put("/cities/{city_id}/", response_model=schemas.CityIn)
async def edit_city(city_id: int, city: schemas.CityIn, db: CommonDB) -> schemas.CityIn:
    return await crud.update_city(db=db, city_id=city_id, payload_city=city)


@router.patch("/cities/{city_id}/", response_model=schemas.CityPatch)
async def partial_edit_city(city_id: int, city: schemas.CityPatch, db: CommonDB):
    return await crud.partial_update_city(db=db, city_id=city_id, payload_city=city)


@router.delete("/cities/{city_id}/", response_model=schemas.CityIn)
async def delete_city(city_id: int, db: CommonDB) -> schemas.CityIn:
    return await crud.delete_city(db=db, city_id=city_id)
