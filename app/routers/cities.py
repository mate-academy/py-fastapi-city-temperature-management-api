from fastapi import APIRouter, HTTPException, status
from db import crud
from db.schemas import CityDTO, CityAddDTO, CityRelDTO
from tools.tools import DataBase

CityDoesntExistError = HTTPException(status_code=404, detail="City not found!")
CityExistError = HTTPException(status_code=400, detail="City with same name already exists!")

cities_router = APIRouter()


@cities_router.get("/cities", response_model=list[CityRelDTO])
async def get_all_cities(
    db: DataBase
):
    return await crud.select_all_cities(db=db)


@cities_router.get("/cities/{city_id}", response_model=CityRelDTO)
async def get_city_by_id(
    db: DataBase,
    city_id: int
):
    selected_city = await crud.select_city_by_id(db=db, city_id=city_id)

    if not selected_city:
        raise CityDoesntExistError

    return selected_city


@cities_router.post("/cities", response_model=CityDTO)
async def post_city(
    db: DataBase,
    city_model: CityAddDTO
):
    city_with_same_name = await crud.select_city_by_name(db=db, name=city_model.name)

    if city_with_same_name:
        raise CityExistError

    return await crud.create_city(db=db, city_model=city_model)


@cities_router.put("/cities/{city_id}", response_model=CityRelDTO)
async def put_city(
    db: DataBase,
    city_id: int,
    city_model: CityAddDTO
):
    city_by_id = await crud.select_city_by_id(db=db, city_id=city_id)

    if not city_by_id:
        raise CityDoesntExistError

    city_wit_same_name = await crud.select_city_by_name(db=db, name=city_model.name)

    if city_wit_same_name and city_wit_same_name.id != city_by_id.id:
        raise CityExistError
    
    return await crud.update_city(db=db, city_to_update=city_by_id, city_model=city_model)


@cities_router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_city(
        db: DataBase,
        city_id: int
):
    city_by_id = await crud.select_city_by_id(db=db, city_id=city_id)

    if not city_by_id:
        raise CityDoesntExistError
    
    await crud.remove_city(db=db, city_to_remove=city_by_id)
    return
