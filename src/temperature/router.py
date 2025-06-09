from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_db

from . import schemas, crud, utils
from src.cities import crud as cities_crud
from src.cities.router import validate_city_exists


router = APIRouter()


@router.get(
    "/temperatures/", 
    response_model=list[schemas.Temperature],
    description=(
        "This endpoint to retrieve the history "
        "of all temperature data."
    )
)
async def get_list_temperatures(
    city_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    if city_id:
        city = await validate_city_exists(db=db, city_id=city_id)
    
    return await crud.get_all_temperatures(db=db, city_id=city_id)


@router.post(
    "/temperatures/update/", 
    status_code=201,
    description=(
        "This endpoint get current temperature data for all cities in the database "
        "from  APIWeather and stores this data in the database."
    )
)
async def temperatures_update(
    db: AsyncSession = Depends(get_db)
):
    cities = await cities_crud.get_all_cities(db=db)

    for city in cities:
        temperature = await utils.fetch_temperature(city.name)
        print(f"{city.name=}, {temperature=}")
        await crud.create_new_item_temperature(db=db, city_id=city.id, temperature=temperature)

    return {"message": "Temperatures updated successfully"}
